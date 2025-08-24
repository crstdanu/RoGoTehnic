document.addEventListener('DOMContentLoaded', function () {
    let currentFetchController = null;
    let requestCounter = 0;
    function filterUATByJudet() {
        if (typeof window.lucrareJudetId !== 'undefined' && window.lucrareJudetId) {
            loadUAT(String(window.lucrareJudetId));
        }
    }

    function loadUAT(judetId) {
        const emitent = document.getElementById('id_emitent');
        if (!emitent) return;
        const thisRequestId = ++requestCounter;
        // anulează cererea anterioară dacă există
        if (currentFetchController) {
            currentFetchController.abort();
        }
        const currentEmitent = emitent.value;
        // stări de încărcare
        emitent.disabled = true;
        emitent.setAttribute('aria-busy', 'true');
        emitent.innerHTML = '';
        const controller = new AbortController();
        currentFetchController = controller;
        const expectedJudetId = judetId;

        fetch(`/ajax/get_uat/?judet_id=${encodeURIComponent(judetId)}`, { signal: controller.signal })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                // dacă între timp s-a schimbat selecția sau cererea a fost depășită, ignorăm
                if (thisRequestId !== requestCounter || expectedJudetId !== String(judetId)) {
                    return;
                }
                const frag = document.createDocumentFragment();
                const placeholder = document.createElement('option');
                placeholder.value = '';
                placeholder.textContent = '---------';
                frag.appendChild(placeholder);

                data.forEach(uat => {
                    const opt = document.createElement('option');
                    opt.value = String(uat.id);
                    opt.textContent = uat.text;
                    frag.appendChild(opt);
                });

                emitent.appendChild(frag);
                if (currentEmitent) {
                    emitent.value = currentEmitent;
                }
            })
            .catch(err => {
                if (err && err.name === 'AbortError') {
                    return; // cerere anulată
                }
                console.error('Eroare la încărcarea UAT:', err);
                // Placeholder fallback
                const placeholder = document.createElement('option');
                placeholder.value = '';
                placeholder.textContent = '---------';
                emitent.innerHTML = '';
                emitent.appendChild(placeholder);
            })
            .finally(() => {
                // re-activăm doar dacă este încă ultimul request
                if (thisRequestId === requestCounter) {
                    emitent.disabled = false;
                    emitent.removeAttribute('aria-busy');
                }
            });
    }

    filterUATByJudet();
});
