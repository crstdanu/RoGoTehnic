from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult

from StudiiFezabilitate.Avize_refactor import avize_bacau as bacau
from StudiiFezabilitate.Avize_refactor import avize_botosani as botosani
from StudiiFezabilitate.Avize_refactor import avize_iasi as iasi
from StudiiFezabilitate.Avize_refactor import avize_neamt as neamt
from StudiiFezabilitate.Avize_refactor import avize_suceava as suceava
from StudiiFezabilitate.Avize_refactor import avize_vaslui as vaslui


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
            if avizCU.nume_aviz.nume == "Aviz APM Neamt":
                return neamt.aviz_APM_Neamt(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Neamț nu poate fi generată (...încă)")

        # BACĂU
        elif lucrare.judet.nume == "Bacău":
            if avizCU.nume_aviz.nume == "Aviz APM Bacau":
                return bacau.aviz_APM_Bacau(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Bacău nu poate fi generată (...încă)")

            # SUCEAVA
        elif lucrare.judet.nume == "Suceava":
            if avizCU.nume_aviz.nume == "Aviz APM Suceava":
                return suceava.aviz_APM_Suceava(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Suceava nu poate fi generată (...încă)")

        # BOTOȘANI
        elif lucrare.judet.nume == "Botoșani":
            if avizCU.nume_aviz.nume == "Aviz APM Botosani":
                return botosani.aviz_APM_Botosani(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Botoșani nu poate fi generată (...încă)")

        # VASLUI
        elif lucrare.judet.nume == "Vaslui":
            if avizCU.nume_aviz.nume == "Aviz APM Vaslui":
                return vaslui.aviz_APM_Vaslui(lucrare_id, id_aviz)
            return DocumentGenerationResult.error_result(
                "Aceasta documentație din Vaslui nu poate fi generată (...încă)")
        else:
            return DocumentGenerationResult.error_result(
                "Documentația nu poate fi generată - nu am documentatii pentru avize din județul lucrării")
    except Exception as e:
        # Captăm excepția și returnăm un rezultat de eroare
        return DocumentGenerationResult.error_result(f"Eroare la crearea fișierelor: {str(e)}")
