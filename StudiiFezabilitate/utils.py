from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult

from StudiiFezabilitate.Avize_refactor import avize_iasi as iasi


def creeaza_fisier(lucrare_id, id_aviz):
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)

        # IASI
        if lucrare.judet.nume == "Iași":
            if avizCU.nume_aviz.nume == "Aviz APM Iasi":
                return iasi.aviz_APM_Iasi(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Iași nu poate fi generată (...încă)")

        # NEAMȚ
        elif lucrare.judet.nume == "Neamț":
            return DocumentGenerationResult.error_result(
                "Aceasta documentație din Neamț nu poate fi generată (...încă)")

        # BACĂU
        elif lucrare.judet.nume == "Bacău":
            return DocumentGenerationResult.error_result(
                "Aceasta documentație din Bacău nu poate fi generată (...încă)")

            # SUCEAVA
        elif lucrare.judet.nume == "Suceava":
            return DocumentGenerationResult.error_result(
                "Aceasta documentație din Suceava nu poate fi generată (...încă)")

        # BOTOȘANI
        elif lucrare.judet.nume == "Botoșani":
            return DocumentGenerationResult.error_result(
                "Aceasta documentație din Botoșani nu poate fi generată (...încă)")

        # VASLUI
        elif lucrare.judet.nume == "Vaslui":
            return DocumentGenerationResult.error_result(
                "Avizul nu poate fi generat - tipul avizului nu este valid")
        else:
            return DocumentGenerationResult.error_result(
                "Documentația nu poate fi generată - nu am documentatii pentru avize din județul lucrării")
    except Exception as e:
        # Captăm excepția și returnăm un rezultat de eroare
        return DocumentGenerationResult.error_result(f"Eroare la crearea fișierelor: {str(e)}")
