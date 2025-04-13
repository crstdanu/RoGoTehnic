from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.services import avize as a
from docxtpl import DocxTemplate
import os
from datetime import datetime
import tempfile


def aviz_APM_iasi(lucrare_id, id_aviz):

    # Obținem lucrarea și avizul din baza de date
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    # Selectăm modelul de cerere în funcție de numele avizului
    if avizCU.nume_aviz.nume == "Aviz APM Iași":
        model_cerere = r"E:\NEW_python\RGT\StudiiFezabilitate\services\TEST\aviz_apm_iasi.docx"
    elif avizCU.nume_aviz.nume == "Aviz EE - DELGAZ Iasi":
        model_cerere = r"E:\NEW_python\RGT\StudiiFezabilitate\services\TEST\aviz_EE_DELGAZ_iasi.docx"
    elif avizCU.nume_aviz.nume == "Aviz GN - DELGAZ Iasi":
        model_cerere = r"E:\NEW_python\RGT\StudiiFezabilitate\services\TEST\aviz_GN_DELGAZ_iasi.docx"
    else:
        # Returnăm un mesaj de eroare dacă nu există model pentru acest aviz
        return "Avizul nu poate fi generat"

    # Verificăm dacă există modelul de cerere
    if not os.path.exists(model_cerere):
        return "Avizul nu poate fi generat - modelul de cerere nu a fost găsit"

    # Pregătim contextul pentru șablon
    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Aviz_{avizCU.nume_aviz}_{lucrare.nume_intern}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul nu poate fi generat - eroare: {str(e)}"
