let timeout = timeout / 1000; // convert to seconds

function startCountdown() {
  const timerElement = document.getElementById("countdown");

  const interval = setInterval(() => {
    timerElement.textContent = `Redirecting in ${timeout} seconds...`;
    timeout--;

    if (timeout === 0) {
      clearInterval(interval);
      timerElement.textContent = "Redirecting...";
      window.location.href = "/"; 
    }
  }, 1000);
}

window.onload = startCountdown;
