document.addEventListener("DOMContentLoaded", () => {
    const avizContainer = document.getElementById("aviz-form");
    if (!avizContainer) return;

    const judetId = avizContainer.dataset.judetId;
    if (judetId) {
        loadAvize(judetId);
    }

    async function loadAvize(judetId) {
        const avizSelect = document.getElementById("id_nume_aviz");
        if (!avizSelect) return;

        const currentAviz = avizSelect.value;
        avizSelect.innerHTML = "";  // goliți opțiunile

        try {
            const response = await fetch(`/ajax/get_avize/?judet_id=${judetId}`);
            if (!response.ok) throw new Error("Eroare la încărcarea avizelor.");

            const data = await response.json();

            // Adaugă opțiunea implicită
            const defaultOption = new Option("---------", "");
            avizSelect.add(defaultOption);

            // Populează opțiunile
            data.forEach(aviz => {
                const option = new Option(aviz.text, aviz.id);
                avizSelect.add(option);
            });

            // Re-selectează opțiunea anterioară, dacă există
            if (currentAviz) {
                avizSelect.value = currentAviz;
            }
        } catch (error) {
            console.error("Eroare la încărcarea avizelor:", error);
        }
    }
});
