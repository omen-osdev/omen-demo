let el;

function startCountdown(time) {
    let remainingTime = time;
    const interval = setInterval(() => {
        remainingTime -= 1;
        if (remainingTime <= 0) {
            clearInterval(interval);
            el.innerHTML = "Session Expired!"
            window.location.href = '/'
            return;
        }
        el.innerHTML = `Session will expire in ${remainingTime} seconds`;
    }, 1000);
}

function getAliveTime() {
    const url = '/instance/time';
    fetch(url)
            .then(response => {
                if (response.status === 403) {
                    el.innerHTML = 'Unavailable session, maybe it is expired?';
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


// Ensuring the DOM is fully loaded before calling getAliveTime
document.addEventListener('DOMContentLoaded', function () {
    el = document.getElementById('countdown');
    getAliveTime();
});
