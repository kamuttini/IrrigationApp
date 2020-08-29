function toggleNav() {
    var e = document.getElementById("sidebar");
    var x = document.getElementsByClassName('nav-text')
    var t = document.getElementsByClassName('navbar-nav')
    if (e.style.width == '20%') {
        e.style.width = '5%';
        for (i = 0; i < x.length; i++)
            x[i].style.display = 'none';

        t[0].style.marginTop = '100%'

    } else {
        e.style.width = '20%';
        for (i = 0; i < x.length; i++)
            x[i].style.display = 'inline';
        t[0].style.marginTop = '30%'
    }
}