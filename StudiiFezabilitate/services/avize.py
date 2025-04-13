from StudiiFezabilitate.models import AvizeCU, Lucrare
from docxtpl import DocxTemplate
import os
from datetime import datetime
import tempfile


def aviz_APM_iasi(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\01. iasi\01. Aviz APM\cerere_aviz_APM_iasi.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul APM iasi - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_APM_Iasi_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul nu poate fi generat - eroare: {str(e)}"


def aviz_APM_neamt(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\02. neamt\01. Aviz APM\cerere_aviz_APM_neamt.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul APM Neamt - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_APM_Neamt_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul APM Neamt nu poate fi generat - eroare: {str(e)}"


def aviz_APM_bacau(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\03. bacau\01. Aviz APM\cerere_aviz_APM_bacau.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul APM Bacau - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_APM_Bacau_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul APM Bacau nu poate fi generat - eroare: {str(e)}"


def aviz_APM_suceava(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\04. suceava\01. Aviz APM\cerere_aviz_APM_suceava.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul APM Suceava - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_APM_Suceava_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul APM Suceava nu poate fi generat - eroare: {str(e)}"


def aviz_APM_botosani(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\05. botosani\01. Aviz APM\cerere_aviz_APM_botosani.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul APM Botosani - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_APM_Botosani_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul APM Botosani nu poate fi generat - eroare: {str(e)}"


def aviz_APM_vaslui(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\06. vaslui\01. Aviz APM\cerere_aviz_APM_vaslui.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul APM Vaslui - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_APM_Vaslui_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul APM Vaslui nu poate fi generat - eroare: {str(e)}"


def aviz_EE_delgaz_iasi(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\01. iasi\02. Aviz EE Delgaz\cerere_aviz_EE_delgaz_iasi.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul EE Delgaz iasi - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_EE_Delgaz_Iasi_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul EE Delgaz Iasi nu poate fi generat - eroare: {str(e)}"


def aviz_EE_delgaz_neamt(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\02. neamt\02. Aviz EE Delgaz\cerere_aviz_EE_delgaz_neamt.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul EE Delgaz Neamt - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_EE_Delgaz_Neamt_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul EE Delgaz Neamt nu poate fi generat - eroare: {str(e)}"


def aviz_EE_delgaz_bacau(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\03. bacau\02. Aviz EE Delgaz\cerere_aviz_EE_delgaz_bacau.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul EE Delgaz Bacau - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_EE_Delgaz_Bacau_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul EE Delgaz Bacau nu poate fi generat - eroare: {str(e)}"


def aviz_EE_delgaz_suceava(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\04. suceava\02. Aviz EE Delgaz\cerere_aviz_EE_delgaz_suceava.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul EE Delgaz Suceava - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_EE_Delgaz_Suceava_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul EE Delgaz Suceava nu poate fi generat - eroare: {str(e)}"


def aviz_EE_delgaz_botosani(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\05. botosani\02. Aviz EE Delgaz\cerere_aviz_EE_delgaz_botosani.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul EE Delgaz Botosani - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_EE_Delgaz_Botosani_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul EE Delgaz Botosani nu poate fi generat - eroare: {str(e)}"


def aviz_EE_delgaz_vaslui(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    try:
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\06. vaslui\02. Aviz EE Delgaz\cerere_aviz_EE_delgaz_vaslui.docx"
    except Exception as e:
        return f"Nu gasesc cererea pentru avizul EE Delgaz Vaslui - eroare: {str(e)}"

    context = {
        'nume_lucrare': lucrare.nume_intern,
        'nr_cu': avizCU.certificat_urbanism.numar,
        'nume_aviz': avizCU.nume_aviz,
    }

    # Creăm directorul temporar dacă este necesar
    temp_dir = tempfile.gettempdir()

    # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
    output_filename = f"Documentatie_Aviz_EE_Delgaz_Vaslui_{lucrare.beneficiar.nume}.docx"
    output_path = os.path.join(temp_dir, output_filename)

    try:
        # Generăm documentul
        doc = DocxTemplate(model_cerere)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as e:
        return f"Avizul EE Delgaz Vaslui nu poate fi generat - eroare: {str(e)}"


# def aviz_GN_delgaz_iasi(lucrare_id, id_aviz):
#     lucrare = Lucrare.objects.get(pk=lucrare_id)
#     avizCU = AvizeCU.objects.get(pk=id_aviz)

#     try:
#         model_cerere = r"StudiiFezabilitate\services\modele_cereri\01. iasi\02. Aviz EE Delgaz\cerere_aviz_EE_delgaz_iasi.docx"
#     except Exception as e:
#         return f"Nu gasesc cererea pentru avizul EE Delgaz iasi - eroare: {str(e)}"

#     context = {
#         'nume_lucrare': lucrare.nume_intern,
#         'nr_cu': avizCU.certificat_urbanism.numar,
#         'nume_aviz': avizCU.nume_aviz,
#     }

#     # Creăm directorul temporar dacă este necesar
#     temp_dir = tempfile.gettempdir()

#     # Generăm numele fișierului cu timestamp pentru a evita suprascrierea
#     output_filename = f"Documentatie_Aviz_EE_Delgaz_Iasi_{lucrare.beneficiar.nume}.docx"
#     output_path = os.path.join(temp_dir, output_filename)

#     try:
#         # Generăm documentul
#         doc = DocxTemplate(model_cerere)
#         doc.render(context)
#         doc.save(output_path)
#         return output_path
#     except Exception as e:
#         return f"Avizul EE Delgaz Iasi nu poate fi generat - eroare: {str(e)}"
