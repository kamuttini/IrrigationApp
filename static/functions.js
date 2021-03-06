// Resize navbar
function toggleNav() {
    var e = document.getElementById("sidebar");
    var x = document.getElementsByClassName('nav-text')
    var ls = document.getElementById("logo-small")
    var lb = document.getElementById("logo-big")

    //on desktop
    if (window.innerWidth > 830 && e.style.width === '5%') {
        e.style.width = 'unset'
        for (i = 0; i < x.length; i++)
            x[i].style.display = 'inline';
        lb.style.display = 'block';
        ls.style.display = 'none';
    } else if (window.innerWidth > 830) {
        e.style.width = '5%'
        for (i = 0; i < x.length; i++)
            x[i].style.display = 'none';
        ls.style.display = 'block';
        lb.style.display = 'none';
    }

    //on mobile
    if (window.innerWidth < 830 && e.style.display === "none") {
        e.style.display = 'block'
        e.style.height = '100vh'
        e.style.position = 'fixed'
        e.style.width = '70%'
    } else if (window.innerWidth < 840) {
        e.style.display = 'none'
    }
}

/*  PAGE REFRESH ON VIEWPORT RESIZE */
window.onresize = function(event)
{
    if (!(window.location.href.indexOf("authentication") > -1)){
        document.location.reload(true);}

}

window.onload = function initial() {
    var e = document.getElementById("sidebar");
    if (window.innerWidth < 840) {
        e.style.display = 'none'
    }
    var ctx = document.getElementById('watering-chart').getContext('2d');
    window.wateringChart = new Chart(ctx, config);
}

// change chart view option

function updateWeek() {
    wateringChart.options.scales.xAxes[0] = {
        type: 'time',
        time: {unit: 'week'}
    };
    wateringChart.update();
}

function updateMonth() {
    wateringChart.options.scales.xAxes[0] = {
        type: 'time',
        time: {unit: 'month'}
    };
    wateringChart.update();
}

function updateDay() {
    wateringChart.options.scales.xAxes[0] = {
        type: 'time',
        time: {unit: 'day'}
    };
    wateringChart.update();
}