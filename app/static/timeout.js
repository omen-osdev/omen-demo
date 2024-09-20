
function displayText(text) {
    const el = document.getElementById('countdown');
    el.innerHTML = text;
}

function startCountdown(time) {
    let remainingTime = time;
    const interval = setInterval(() => {
        remainingTime -= 1;
        if (remainingTime <= 0) {
            clearInterval(interval);
            displayText('Session expired');
            window.location.href = '/'
            return;
        }
        displayText(`Session will expire in ${remainingTime} seconds`);
    }, 1000);
}

function getAliveTime() {
    const url = '/instance/time';
    fetch(url)
            .then(response => {
                if (response.status === 403) {
                    el.innerHTML = 'Unavailable session, maybe it expired?';
                    return;
                }
                if (!response.ok) {
                    el.innerHTML = 'Failed to get alive time, please try again later';
                    return;
                }
                return response.json();
            }).then(data => {
                if(data) {
                    startCountdown(data.alive_time);
                }
                else {
                    el.innerHTML = 'Failed to get alive time, please try again later';
                }
            }
            ).catch(error => {
                el.innerHTML = 'Failed to get alive time, please try again later';
            });
}

window.onload = getAliveTime();
