(function () {
    'use strict';

    /* ---------- scroll reveal ---------- */
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const reveals = document.querySelectorAll('.reveal');
    if (reduce || !('IntersectionObserver' in window)) {
        reveals.forEach(el => el.classList.add('in'));
    } else {
        const io = new IntersectionObserver((entries) => {
            entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
        }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
        reveals.forEach(el => io.observe(el));
    }

    /* ---------- contact form: quote / message modes ---------- */
    const form = document.querySelector('#contact-form');
    if (form) {
        const modeBtns = form.querySelectorAll('.mode-btn');
        const typeField = form.querySelector('#inquiryType');
        modeBtns.forEach(b => b.addEventListener('click', () => {
            modeBtns.forEach(x => x.classList.remove('active'));
            b.classList.add('active');
            const mode = b.dataset.mode;
            form.classList.toggle('show', mode === 'quote');
            if (typeField) typeField.value = mode === 'quote' ? 'Quote request' : 'General inquiry';
        }));
    }
    
})();


