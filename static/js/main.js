function showNavbarList(id) {
    const nav = document.getElementById(id);
    nav.classList.toggle('active')
}

function redirect(url) {
    'use strict';
    const link = document.createElement("a");
    link.href = url;
    link.style.display = "none"; // Hide the link
    document.body.appendChild(link);
    link.click(); // Simulate a click
    document.body.removeChild(link); // Clean up
}

function deleteProduct(ele, url) {
    fetch(url).then(response => {
        if (response.ok) {
            ele.parentNode.parentNode.parentNode.remove();
            cards = document.querySelectorAll('.col-xl-8 .card-body');
            if (cards.length == 0) {
                document.querySelector('div.row').innerHTML = ` <h2 class="text-center">السلة فارغة من المنتوجات. <a href="/">تسوق الآن!</a></h2>`;
            }
        }
    });
}