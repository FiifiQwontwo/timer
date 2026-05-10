from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from django.views import View

from .forms import TimerStateForm
from .models import TimerState


class TimerStateListView(View):

    template_name = "timer_state/list.html"

    def get(self, request):

        timer_states = (
            TimerState.objects
            .select_related("session")
            .all()
        )

        context = {
            "timer_states": timer_states
        }

        return render(
            request,
            self.template_name,
            context
        )


class TimerStateDetailView(View):

    template_name = "timer_state/detail.html"

    def get(self, request, pk):

        timer_state = get_object_or_404(
            TimerState.objects.select_related("session"),
            pk=pk
        )

        context = {
            "timer_state": timer_state
        }

        return render(
            request,
            self.template_name,
            context
        )


class TimerStateCreateView(View):

    template_name = "timer_state/create.html"

    def get(self, request):

        form = TimerStateForm()

        return render(
            request,
            self.template_name,
            {
                "form": form
            }
        )

    def post(self, request):

        form = TimerStateForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Timer state created successfully."
            )

            return redirect(
                "timer:timer_state_list"
            )

        return render(
            request,
            self.template_name,
            {
                "form": form
            }
        )


class TimerStateUpdateView(View):

    template_name = "timer_state/update.html"

    def get(self, request, pk):

        timer_state = get_object_or_404(
            TimerState,
            pk=pk
        )

        form = TimerStateForm(instance=timer_state)

        context = {
            "form": form,
            "timer_state": timer_state
        }

        return render(
            request,
            self.template_name,
            context
        )

    def post(self, request, pk):

        timer_state = get_object_or_404(
            TimerState,
            pk=pk
        )

        form = TimerStateForm(
            request.POST,
            instance=timer_state
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Timer state updated successfully."
            )

            return redirect(
                "timer:timer_state_detail",
                pk=timer_state.pk
            )

        context = {
            "form": form,
            "timer_state": timer_state
        }

        return render(
            request,
            self.template_name,
            context
        )


class TimerStateDeleteView(View):

    def post(self, request, pk):

        timer_state = get_object_or_404(
            TimerState,
            pk=pk
        )

        timer_state.delete()

        messages.success(
            request,
            "Timer state deleted successfully."
        )

        return redirect(
            "timer:timer_state_list"
        )