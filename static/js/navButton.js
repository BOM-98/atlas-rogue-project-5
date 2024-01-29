document.addEventListener('DOMContentLoaded', function() {
    var bttLink = document.querySelector('.btt-link');
    if (bttLink) {
        bttLink.addEventListener('click', function(e) {
            window.scrollTo({
                top: 0,
                left: 0,
                behavior: 'smooth'
            });
        });
    }
});