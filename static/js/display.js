// display.js

const socket = new WebSocket("ws://" + window.location.host + "/ws/timer/");

const timerEl = document.getElementById("timer");
const presetEl = document.getElementById("preset-name");
const timeUpEl = document.getElementById("time-up");

let blinkInterval = null;

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    const { remaining, status, preset } = data;

    presetEl.innerText = preset || "";

    if (status === "TIME_UP") {
        showTimeUp();
        return;
    }

    hideTimeUp();

    timerEl.innerText = formatTime(remaining);
    updateColor(remaining);
};

function formatTime(seconds) {
    let m = Math.floor(seconds / 60);
    let s = seconds % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
}

function updateColor(remaining) {
    document.body.className = "";

    if (remaining > 60) {
        document.body.classList.add("green");
    } else if (remaining > 10) {
        document.body.classList.add("yellow");
    } else {
        document.body.classList.add("red");
    }
}

function showTimeUp() {
    timerEl.style.display = "none";
    timeUpEl.classList.remove("hidden");

    let visible = true;

    if (!blinkInterval) {
        blinkInterval = setInterval(() => {
            timeUpEl.style.visibility = visible ? "hidden" : "visible";
            visible = !visible;
        }, 500);
    }
}

function hideTimeUp() {
    timerEl.style.display = "block";
    timeUpEl.classList.add("hidden");

    if (blinkInterval) {
        clearInterval(blinkInterval);
        blinkInterval = null;
    }
}