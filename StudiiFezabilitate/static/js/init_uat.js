$(document).ready(function () {
    function filterUATByJudet() {
        if (typeof window.lucrareJudetId !== 'undefined') {
            loadUAT(window.lucrareJudetId);
        }
    }

    function loadUAT(judetId) {
        if ($('#id_emitent').length) {
            var currentEmitent = $('#id_emitent').val();
            $('#id_emitent').empty();

            fetch(`/ajax/get_uat/?judet_id=${judetId}`)
                .then(response => response.json())
                .then(data => {
                    $('#id_emitent').append($('<option>', {
                        value: '',
                        text: '---------'
                    }));

                    data.forEach(function (uat) {
                        $('#id_emitent').append($('<option>', {
                            value: uat.id,
                            text: uat.text
                        }));
                    });

                    if (currentEmitent) {
                        $('#id_emitent').val(currentEmitent);
                    }
                });
        }
    }

    filterUATByJudet();
});
