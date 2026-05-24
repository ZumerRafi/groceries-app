function previewImage(event){

    const image = document.getElementById('preview');

    image.src = URL.createObjectURL(event.target.files[0]);

    image.style.display = 'block';
}


/* IMAGE MODAL */

function openModal(src){

    document.getElementById('modal').style.display = 'block';

    document.getElementById('modal-img').src = src;
}


function closeModal(){

    document.getElementById('modal').style.display = 'none';
}


window.onclick = function(event){

    const modal = document.getElementById('modal');

    if(event.target == modal){

        modal.style.display = 'none';
    }
}


/* DELETE CONFIRMATION */

function confirmDelete(){

    return confirm(
        'Are you sure you want to delete this expense?'
    );
}


/* AUTO HIDE ALERTS */

window.addEventListener('DOMContentLoaded', () => {

    setTimeout(() => {

        const alerts = document.querySelectorAll('.alert');

        alerts.forEach(alert => {

            alert.style.opacity = '0';

            alert.style.transform = 'translateX(100px)';

            setTimeout(() => {

                alert.remove();

            }, 500);

        });

    }, 3000);

});


/* THEME TOGGLE */

function toggleTheme(){

    document.body.classList.toggle('light-mode');

    localStorage.setItem(
        'theme',
        document.body.classList.contains('light-mode')
    );
}


/* LOAD SAVED THEME */

window.onload = function(){

    if(localStorage.getItem('theme') === 'true'){

        document.body.classList.add('light-mode');
    }

}


/* MOBILE SIDEBAR */

function toggleMenu(){

    document.querySelector('.sidebar').classList.toggle('active');
}


/* CLOSE SIDEBAR ON MOBILE LINK CLICK */

const sidebarLinks = document.querySelectorAll('.sidebar a');

sidebarLinks.forEach(link => {

    link.addEventListener('click', () => {

        if(window.innerWidth <= 900){

            document
                .querySelector('.sidebar')
                .classList.remove('active');
        }
    });
});


/* SMOOTH CARD HOVER */

const cards = document.querySelectorAll('.card');

cards.forEach(card => {

    card.addEventListener('mouseenter', () => {

        card.style.transform = 'translateY(-8px) scale(1.02)';
    });

    card.addEventListener('mouseleave', () => {

        card.style.transform = 'translateY(0px) scale(1)';
    });

});


/* PAGE FADE IN */

document.body.style.opacity = 0;

window.addEventListener('load', () => {

    document.body.style.transition = '0.5s';

    document.body.style.opacity = 1;
});
/* LOADER */

window.addEventListener('load', () => {

    setTimeout(() => {

        const loader = document.getElementById('loader');

        loader.style.opacity = '0';

        setTimeout(() => {

            loader.style.display = 'none';

        }, 500);

    }, 1800);

});