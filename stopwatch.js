/* Used to simulate a stopwatch. */
var h3 = document.getElementsByTagName('h3')[0],
    start = document.getElementById('start'),
    stop = document.getElementById('stop'),
    reset = document.getElementById('reset'),
    seconds = 0, minutes = 0, hours = 0,
    t;

function add() {
    seconds++;
    if (seconds >= 60) {
        seconds = 0;
        minutes++;
        if (minutes >= 60) {
            minutes = 0;
            hours++;
        }
    }
    
    h3.textContent = (hours ? (hours > 9 ? hours : "0" + hours) : "00") + ":" 
                   + (minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00") + ":" 
                   + (seconds > 9 ? seconds : "0" + seconds);

    timer(); /* Mutual recursion between add and timer function. */
}
function timer() {
    t = setTimeout(add, 1000); /* Evaluates add function every second. */
}


/* Start button */
start.onclick = timer;

/* Stop button */
stop.onclick = function() {
    clearTimeout(t);
}

/* Reset button */
reset.onclick = function() {
    clearTimeout(t)
    h3.textContent = "00:00:00";
    seconds = 0; minutes = 0; hours = 0;
}
