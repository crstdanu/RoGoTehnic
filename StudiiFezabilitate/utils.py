from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.services import avize as a
from StudiiFezabilitate.result import DocumentGenerationResult


def creeaza_fisier(lucrare_id, id_aviz):
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)

        if lucrare.judet.nume == "Iași":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return a.aviz_APM_iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = a.aviz_EE_delgaz_iasi(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație nu poate fi generată (...încă)")
        elif lucrare.judet.nume == "Neamț":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return a.aviz_APM_neamt(lucrare.id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = a.aviz_EE_delgaz_neamt(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Avizul nu poate fi generat - tipul avizului nu este valid")
        elif lucrare.judet.nume == "Bacău":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return a.aviz_APM_bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = a.aviz_EE_delgaz_bacau(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Avizul nu poate fi generat - tipul avizului nu este valid")
        elif lucrare.judet.nume == "Suceava":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return a.aviz_APM_suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = a.aviz_EE_delgaz_suceava(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Avizul nu poate fi generat - tipul avizului nu este valid")
        elif lucrare.judet.nume == "Botoșani":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return a.aviz_APM_botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = a.aviz_EE_delgaz_botosani(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Avizul nu poate fi generat - tipul avizului nu este valid")
        elif lucrare.judet.nume == "Vaslui":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return a.aviz_APM_vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = a.aviz_EE_delgaz_vaslui(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Avizul nu poate fi generat - tipul avizului nu este valid")
        else:
            return DocumentGenerationResult.error_result(
                "Documentația nu poate fi generată - nu am documentatii pentru avize din județul lucrării")
    except Exception as e:
        # Captăm excepția și returnăm un rezultat de eroare
        return DocumentGenerationResult.error_result(f"Eroare la crearea fișierelor: {str(e)}")
