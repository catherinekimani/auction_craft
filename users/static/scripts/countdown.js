// countdown.js

function startCountdown(elementId, endDate) {
    var countdownElement = document.getElementById(elementId);

    function updateCountdown() {
        var now = new Date().getTime();
        var distance = endDate - now;

        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        countdownElement.innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

        if (distance < 0) {
            countdownElement.innerHTML = "Expired";
        }
    }

    setInterval(updateCountdown, 1000);

    updateCountdown();
}

var endDate1 = new Date("December 25, 2023 10:00:00").getTime();
var endDate2 = new Date("December 31, 2023 18:30:00").getTime();
var endDate3 = new Date("January 15, 2024 12:00:00").getTime();
var endDate4 = new Date("February 1, 2024 20:00:00").getTime();
var endDate5 = new Date("March 10, 2024 15:45:00").getTime();
var endDate6 = new Date("April 5, 2024 09:30:00").getTime();

startCountdown("countdown1", endDate1);
startCountdown("countdown2", endDate2);
startCountdown("countdown3", endDate3);
startCountdown("countdown4", endDate4);
startCountdown("countdown5", endDate5);
startCountdown("countdown6", endDate6);
