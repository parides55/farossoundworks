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
    const form = document.querySelector('.form');
    if (form) {
        const modeBtns = form.querySelectorAll('.mode-btn');
        const typeField = form.querySelector('#inquiryType');
        modeBtns.forEach(b => b.addEventListener('click', () => {
            modeBtns.forEach(x => x.classList.remove('active'));
            b.classList.add('active');
            const mode = b.dataset.mode;
            form.classList.toggle('mode-quote', mode === 'quote');
            if (typeField) typeField.value = mode === 'quote' ? 'Quote request' : 'General inquiry';
        }));
    }

    const input = document.getElementById("file-upload");
    const store = new DataTransfer();
    const list = document.getElementById("file-list");

    input.addEventListener("change", () => {
        // Add newly picked files to our running store
        for (const file of input.files) {
            // avoid duplicates by name+size
            const exists = Array.from(store.files).some(
                f => f.name === file.name && f.size === file.size
            );
            if (!exists) store.items.add(file);
        }

        // Write the accumulated set back onto the input
        input.files = store.files;

        // Show current selection
        list.innerHTML = "";
        for (const f of store.files) {
            const li = document.createElement("li");
            li.textContent = f.name;
            list.appendChild(li);
        }
    });
    
})();


