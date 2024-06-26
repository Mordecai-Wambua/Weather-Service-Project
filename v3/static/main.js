document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('dashboard-link').addEventListener('click', function (event) {
        event.preventDefault();
        showContent('weather-content');
    });

    document.getElementById('support-link').addEventListener('click', function (event) {
        event.preventDefault();
        showContent('support-content');
    });

    document.getElementById('about-link').addEventListener('click', function (event) {
        event.preventDefault();
        showContent('about-content');
    });

    function showContent(contentId) {
        const contents = document.querySelectorAll('.dash');
        contents.forEach(content => {
            if (content.id === contentId) {
                content.style.display = 'block';
            } else {
                content.style.display = 'none';
            }
        });
    }

    // add hovered class to selected list item
    let list = document.querySelectorAll('.navigation li');

    function activeLink() {
        list.forEach((item) => {
            item.classList.remove('hovered');
        });
        this.classList.add('hovered');
    }

    list.forEach(item => item.addEventListener('mouseover', activeLink));

    // Menu Toggle
    let toggle = document.querySelector('.toggle');
    let navigation = document.querySelector('.navigation');
    let main = document.querySelector('.main');

    toggle.onclick = function () {
        navigation.classList.toggle('active');
        main.classList.toggle('active');
    }

});