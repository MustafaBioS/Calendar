const calendar = document.querySelector(".calendar"),
    date = document.querySelector('.date'),
    daysCon = document.querySelector('.days'),
    prev = document.querySelector('.prev'),
    next = document.querySelector('.next');

let today = new Date();
let activeDay;
let month = today.getMonth();
let year = today.getFullYear()


const calbtn = document.querySelector('.calbtn');
right = document.querySelector('.rightPart');
rightOn = false


const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
];

function Calendar() {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const prevLastDay = new Date(year, month, 0);
    const prevDays = prevLastDay.getDate();
    const lastDate = lastDay.getDate();
    const day = firstDay.getDay();
        const nextDays = 7 - lastDay.getDay() - 1;

        date.innerHTML = months[month] + " " + year;

        let days = "";

        for (let x = day; x > 0; x--) {
            days += `<div class="day prev-date">${prevDays - x + 1}</div>`;
        }

        for (let i = 1; i <= lastDate; i++) {
            if (i == new Date().getDate() && year == new Date().getFullYear() && month == new Date().getMonth()) {
                days += `<div class="day active today">${i}</div>`;
            }
            
            else {
                days += `<div class="day">${i}</div>`;
            }
        }

            for (let j = 1; j <= nextDays; j++){
                days += `<div class="day next-date">${j}</div>`;
            }

        daysCon.innerHTML = days;

        const prevDate = document.querySelectorAll('.prev-date');
        const nextDate = document.querySelectorAll('.next-date');

        prevDate.forEach(date => {
            date.addEventListener('click', ()=> {
                prevMonth();
            });
        });

        nextDate.forEach(date => {
            date.addEventListener('click', ()=> {
                nextMonth();
            });
        });
}

Calendar();

function prevMonth() {
    month--;
    if (month < 0) {
        month = 11;
        year--;
    }
    Calendar();
}

function nextMonth() {
    month++;
    if (month > 11) {
        month = 0;
        year++;
    }
    Calendar();
}


prev.addEventListener('click', ()=> {
    prevMonth();
})

next.addEventListener('click', ()=> {
    nextMonth();
})

calbtn.addEventListener('click', (e) => {
  e.stopPropagation();
  if (!rightOn) {
    right.classList.add('open');
    rightOn = true;
  } else {
    right.classList.remove('open');
    rightOn = false;
  }
});

right.addEventListener('click', (e) => {
  e.stopPropagation();
});
