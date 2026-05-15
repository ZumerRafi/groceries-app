function previewImage(event){

    const image = document.getElementById('preview');

    image.src = URL.createObjectURL(event.target.files[0]);

    image.style.display = 'block';
}


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


function confirmDelete(){

    return confirm(
        'Are you sure you want to delete this expense?'
    );
}


window.addEventListener('DOMContentLoaded', () => {

    setTimeout(() => {

        const alerts = document.querySelectorAll('.alert');

        alerts.forEach(alert => {

            alert.style.opacity = '0';

            setTimeout(() => {

                alert.remove();

            }, 500);

        });

    }, 3000);

});


function toggleTheme(){

    document.body.classList.toggle('light-mode');

    localStorage.setItem(
        'theme',
        document.body.classList.contains('light-mode')
    );
}


window.onload = function(){

    if(localStorage.getItem('theme') === 'true'){

        document.body.classList.add('light-mode');
    }

}