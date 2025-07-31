document.addEventListener('DOMContentLoaded', function() {
    const judetSelect = document.getElementById('id_judet');
    const localitateSelect = document.getElementById('id_localitate');
    
    // Funcție pentru a încărca localitățile în funcție de județ
    function loadLocalitati(judetId, selectedLocalitateId = null) {
        // Golește dropdown-ul existent
        localitateSelect.innerHTML = '<option value="">---------</option>';
        
        if (!judetId) return;
        
        // Solicită localitățile pentru județul selectat
        fetch(`/ajax/get_localitati/?judet_id=${judetId}`)
            .then(response => response.json())
            .then(data => {
                // Adaugă opțiunile la dropdown
                data.forEach(localitate => {
                    const option = document.createElement('option');
                    option.value = localitate.id;
                    option.textContent = localitate.text;
                    
                    // Selectează valoarea inițială dacă există
                    if (selectedLocalitateId && localitate.id == selectedLocalitateId) {
                        option.selected = true;
                    }
                    
                    localitateSelect.appendChild(option);
                });
            });
    }
    
    // La schimbarea județului, încarcă localitățile corespunzătoare
    judetSelect.addEventListener('change', function() {
        loadLocalitati(this.value);
    });
    
    // Încarcă localitățile inițiale dacă există un județ selectat
    if (judetSelect.value) {
        const initialLocalitateId = localitateSelect.value;
        loadLocalitati(judetSelect.value, initialLocalitateId);
    }
});
