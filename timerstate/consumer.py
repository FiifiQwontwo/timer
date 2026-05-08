import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from asgiref.sync import sync_to_async
from .models import TimerState


class TimerConsumer(AsyncWebsocketConsumer):
    """
    Real-time church timer consumer.

    Features:
    - Start / Pause / Reset / Next
    - TIME_UP state
    - Auto-next after 10 seconds
    - Shared websocket broadcast
    """

    group_name = "timer_group"
    timer_task = None

    # =========================================================
    # CONNECTIONS
    # =========================================================

    async def connect(self):
        """
        Called when websocket connects.
        """

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # Send current timer state immediately
        await self.send_current_state()

        # Start ONE global timer loop
        if TimerConsumer.timer_task is None:
            TimerConsumer.timer_task = asyncio.create_task(
                self.timer_loop()
            )

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):

        if not text_data:
            return

        data = json.loads(text_data)
        action = data.get("action")

        actions = {
            "START": self.start_timer,
            "PAUSE": self.pause_timer,
            "RESET": self.reset_timer,
            "NEXT": self.next_preset,
        }

        handler = actions.get(action)

        if handler:
            await handler()

    # =========================================================
    # DATABASE HELPERS
    # =========================================================

    @sync_to_async
    def get_state(self):
        """
        Get active timer state.
        """

        return (
            TimerState.objects
            .select_related("session")
            .filter(session__is_active=True)
            .first()
        )

    @sync_to_async
    def save_state(self, state):
        """
        Save timer state.
        """

        state.save()

    @sync_to_async
    def get_items(self, state):
        """
        Get ordered queue items.
        """

        return list(
            state.session.items
            .select_related("preset")
            .order_by("order")
        )

    async def start_timer(self):
        """
        Start or resume timer.
        """

        state = await self.get_state()

        if not state:
            return

        if state.status in ["IDLE", "PAUSED"]:

            # Prevent starting empty timer
            if state.remaining_time <= 0:
                items = await self.get_items(state)

                if state.current_index < len(items):
                    current_item = items[state.current_index]
                    state.remaining_time = current_item.preset.duration

            state.status = "RUNNING"
            state.started_at = timezone.now()

            await self.save_state(state)

        await self.broadcast_state()

    async def pause_timer(self):
        """
        Pause running timer.
        """

        state = await self.get_state()

        if not state:
            return

        if state.status == "RUNNING" and state.started_at:
            elapsed = int(
                (timezone.now() - state.started_at).total_seconds()
            )

            state.remaining_time = max(
                0,
                state.remaining_time - elapsed
            )

            state.status = "PAUSED"

            await self.save_state(state)

        await self.broadcast_state()

    async def reset_timer(self):
        """
        Reset current preset timer.
        """

        state = await self.get_state()

        if not state:
            return

        items = await self.get_items(state)

        if state.current_index < len(items):
            current_item = items[state.current_index]

            state.remaining_time = current_item.preset.duration
            state.status = "IDLE"
            state.started_at = None
            state.time_up_started_at = None

            await self.save_state(state)

        await self.broadcast_state()

    async def next_preset(self):
        """
        Move to next preset in queue.
        """

        state = await self.get_state()

        if not state:
            return

        items = await self.get_items(state)

        state.current_index += 1

        # Queue finished
        if state.current_index >= len(items):
            state.status = "IDLE"
            state.remaining_time = 0
            state.started_at = None
            state.time_up_started_at = None

            await self.save_state(state)
            await self.broadcast_state()

            return

        # Load next preset
        next_item = items[state.current_index]

        state.remaining_time = next_item.preset.duration
        state.status = "RUNNING"
        state.started_at = timezone.now()
        state.time_up_started_at = None

        await self.save_state(state)
        await self.broadcast_state()

    async def timer_loop(self):
        """
        Global timer engine.

        Runs continuously every second.
        """

        while True:

            await asyncio.sleep(1)

            state = await self.get_state()

            if not state:
                continue

            now = timezone.now()

            if state.status == "RUNNING":

                if not state.started_at:
                    continue

                elapsed = int(
                    (now - state.started_at).total_seconds()
                )

                remaining = max(
                    0,
                    state.remaining_time - elapsed
                )

                # Timer reached zero
                if remaining <= 0:
                    state.status = "TIME_UP"
                    state.remaining_time = 0
                    state.time_up_started_at = now

                    await self.save_state(state)

                await self.broadcast_state()

            elif state.status == "TIME_UP":

                if not state.time_up_started_at:
                    continue

                diff = int(
                    (now - state.time_up_started_at).total_seconds()
                )

                # Auto move after 10 seconds
                if diff >= 10:
                    await self.next_preset()

                await self.broadcast_state()

    async def broadcast_state(self):
        """
        Broadcast timer state to all websocket clients.
        """

        state = await self.get_state()

        if not state:
            return

        items = await self.get_items(state)

        preset_name = None

        if state.current_index < len(items):
            preset_name = items[state.current_index].preset.name

        # Calculate live remaining time
        live_remaining = state.remaining_time

        if state.status == "RUNNING" and state.started_at:
            elapsed = int(
                (timezone.now() - state.started_at).total_seconds()
            )

            live_remaining = max(
                0,
                state.remaining_time - elapsed
            )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "timer_update",
                "data": {
                    "status": state.status,
                    "remaining": live_remaining,
                    "preset": preset_name,
                    "current_index": state.current_index,
                }
            }
        )

    async def timer_update(self, event):
        """
        Send websocket update to client.
        """

        await self.send(
            text_data=json.dumps(event["data"])
        )

    async def send_current_state(self):
        """
        Send current timer state on connect.
        """

        await self.broadcast_state()
