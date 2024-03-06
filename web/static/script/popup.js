const images = [...document.querySelectorAll('.image')];

// popup

const popup = document.querySelector('.popup');
const closeBtn = document.querySelector('.close-btn');
const largeImage = document.querySelector('.large-image');


popup.addEventListener('click', (e) => {

    const bound = largeImage.getBoundingClientRect();
    const x = e.clientX;
    const y = e.clientY;

    if (!(x >= bound.left && x <= bound.right &&
        y >= bound.top && y <= bound.bottom)) {
        popup.classList.toggle('active');u
    }
});

images.forEach((item, i) => {
    item.addEventListener('click', () => {

        largeImage.src = item.src;
        popup.classList.toggle('active');
    })
})


closeBtn.addEventListener('click', () => {
    popup.classList.toggle('active');
})