document.addEventListener('DOMContentLoaded', function () {
    const judetSelect = document.getElementById('id_judet');
    const localitateSelect = document.getElementById('id_localitate');
    const getLocalitatiUrl = (window.GET_LOCALITATI_URL || '/ajax/get_localitati/');
    let currentFetchController = null; // pentru anularea cererilor anterioare
    let requestCounter = 0; // token pentru a ignora răspunsuri întârziate

    if (!(judetSelect && localitateSelect)) return;

    function updateLocalitati() {
        const judetId = judetSelect.value;
        const desiredSelectedId = localitateSelect.dataset.selected || (window.selectedLocalitateId || '');
        const thisRequestId = ++requestCounter;

        if (currentFetchController) {
            currentFetchController.abort();
        }

        if (!judetId) {
            // Integrare cu Tom Select dacă este activ
            if (localitateSelect.tomselect) {
                localitateSelect.tomselect.clear();
                localitateSelect.tomselect.clearOptions();
                localitateSelect.tomselect.addOption({ value: '', text: '---------' });
            } else {
                localitateSelect.innerHTML = '<option value="">---------</option>';
            }
            localitateSelect.disabled = true;
            localitateSelect.removeAttribute('aria-busy');
            return;
        }

        localitateSelect.disabled = true;
        localitateSelect.setAttribute('aria-busy', 'true');
        if (localitateSelect.tomselect) {
            localitateSelect.tomselect.clearOptions();
            localitateSelect.tomselect.addOption({ value: '', text: 'Se încarcă…' });
            localitateSelect.tomselect.refreshOptions(false);
        } else {
            localitateSelect.innerHTML = '<option selected disabled>Se încarcă…</option>';
        }

        const controller = new AbortController();
        currentFetchController = controller;
        const expectedJudetId = judetId;

        const url = `${getLocalitatiUrl}?judet_id=${encodeURIComponent(judetId)}`;

        fetch(url, { signal: controller.signal })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                if (judetSelect.value !== expectedJudetId || thisRequestId !== requestCounter) {
                    return;
                }
                if (localitateSelect.tomselect) {
                    const ts = localitateSelect.tomselect;
                    ts.clear();
                    ts.clearOptions();
                    ts.addOption({ value: '', text: '---------' });
                    // add all options
                    const options = data.map(item => ({ value: String(item.id), text: item.text }));
                    ts.addOptions(options);
                    ts.refreshOptions(false);
                    if (desiredSelectedId) {
                        const val = String(desiredSelectedId);
                        const exists = options.some(o => o.value === val);
                        if (exists) ts.setValue(val, true);
                    }
                } else {
                    const frag = document.createDocumentFragment();
                    const placeholder = document.createElement('option');
                    placeholder.value = '';
                    placeholder.textContent = '---------';
                    frag.appendChild(placeholder);

                    data.forEach(item => {
                        const option = document.createElement('option');
                        option.value = String(item.id);
                        option.textContent = item.text;
                        frag.appendChild(option);
                    });

                    localitateSelect.innerHTML = '';
                    localitateSelect.appendChild(frag);

                    if (desiredSelectedId) {
                        const val = String(desiredSelectedId);
                        const hasOption = Array.from(localitateSelect.options).some(opt => opt.value === val);
                        if (hasOption) {
                            localitateSelect.value = val;
                        }
                    }
                }
            })
            .catch(err => {
                if (err && err.name === 'AbortError') return;
                console.error('Eroare la încărcarea localităților:', err);
                if (localitateSelect.tomselect) {
                    localitateSelect.tomselect.clear();
                    localitateSelect.tomselect.clearOptions();
                    localitateSelect.tomselect.addOption({ value: '', text: '---------' });
                } else {
                    localitateSelect.innerHTML = '<option value="">---------</option>';
                }
            })
            .finally(() => {
                if (judetSelect.value === expectedJudetId && thisRequestId === requestCounter) {
                    localitateSelect.disabled = false;
                    localitateSelect.removeAttribute('aria-busy');
                }
            });
    }

    if (judetSelect.value) {
        updateLocalitati();
    } else {
        localitateSelect.disabled = true;
    }

    judetSelect.addEventListener('change', updateLocalitati);
});
