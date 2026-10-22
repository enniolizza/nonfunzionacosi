/* Progressive enhancement: without JavaScript every panel remains readable. */
(() => {
    'use strict';
    const carousel = document.querySelector('#banner-carousel');
    if (!carousel) return;

    const slides = [...carousel.querySelectorAll('.banner-slide')];
    const controls = carousel.querySelector('.banner-dots');
    const buttons = [...carousel.querySelectorAll('[data-slide]')];
    if (!controls || !slides.length || buttons.length !== slides.length) return;

    function showSlide(index) {
        slides.forEach((slide, position) => {
            const selected = position === index;
            slide.hidden = !selected;
            slide.classList.toggle('active', selected);
            buttons[position].classList.toggle('active', selected);
            buttons[position].setAttribute('aria-pressed', String(selected));
        });
    }

    buttons.forEach((button, index) => {
        slides[index].id = `banner-panel-${index + 1}`;
        button.setAttribute('aria-controls', slides[index].id);
        button.addEventListener('click', () => showSlide(index));
        button.addEventListener('keydown', (event) => {
            const target = {
                ArrowRight: (index + 1) % slides.length,
                ArrowLeft: (index + slides.length - 1) % slides.length,
                Home: 0,
                End: slides.length - 1,
            }[event.key];
            if (target === undefined) return;
            event.preventDefault();
            showSlide(target);
            buttons[target].focus();
        });
    });

    // User-controlled navigation avoids forced motion and unexpected changes.
    carousel.classList.add('is-enhanced');
    showSlide(0);
    controls.hidden = false;
})();
