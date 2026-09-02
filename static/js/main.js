let mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

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
    const list = document.getElementById("file-list");

    if (input && list) {
        let store = new DataTransfer();

        input.addEventListener("change", () => {
            for (const file of input.files) {
                const exists = Array.from(store.files).some(
                    f => f.name === file.name && f.size === file.size
                );
                if (!exists) store.items.add(file);
            }
            input.files = store.files;
            render();
        });

        function render() {
            list.innerHTML = "";
            Array.from(store.files).forEach((f, index) => {
                const li = document.createElement("li");
                li.textContent = f.name + " ";
                const btn = document.createElement("button");
                btn.type = "button";
                btn.textContent = "✕";
                btn.addEventListener("click", () => removeFile(index));
                li.appendChild(btn);
                list.appendChild(li);
            });
        }

        function removeFile(index) {
            const next = new DataTransfer();
            Array.from(store.files).forEach((f, i) => {
                if (i !== index) next.items.add(f);
            });
            store = next;
            input.files = store.files;
            render();
        }
    }

    /* ---------- work filtering ---------- */
    const filters = document.querySelectorAll('.filter');
    const cards = document.querySelectorAll('.card');
    filters.forEach(btn => btn.addEventListener('click', () => {
        console.log('filter clicked');
        console.log(filters, cards);
        filters.forEach(f => f.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.dataset.filter;
        cards.forEach(card => {
            const match = cat === 'all' || card.dataset.cat === cat;
            card.classList.toggle('hide', !match);
        });
    }));

})();