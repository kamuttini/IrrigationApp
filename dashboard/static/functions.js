function toggleNav() {
    var e = document.getElementById("sidebar");
    var x = document.getElementsByClassName('nav-text')
    var t = document.getElementsByClassName('navbar-nav')
    var l = document.getElementById("logo")
    if (e.style.width === '20%') {
        e.style.width = '5%';
        for (i = 0; i < x.length; i++)
            x[i].style.display = 'none';
        l.style.display = 'none'
        t[0].style.marginTop = '100%'

    } else {
        e.style.width = '20%';
        for (i = 0; i < x.length; i++)
            x[i].style.display = 'inline';
        l.style.display = 'block';
        t[0].style.marginTop = '30%'
    }
}