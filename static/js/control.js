// control.js

const socket = new WebSocket("ws://" + window.location.host + "/ws/timer/");

function sendAction(action) {
    socket.send(JSON.stringify({ action }));
}

// ENTER → NEXT
document.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendAction("NEXT");
    }
});