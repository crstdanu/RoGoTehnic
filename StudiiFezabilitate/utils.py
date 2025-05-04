from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.Avize.Common import avize as common
from StudiiFezabilitate.result import DocumentGenerationResult


def creeaza_fisier(lucrare_id, id_aviz):
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)

        if "Aviz APM" in avizCU.nume_aviz.nume:
            return common.aviz_APM(lucrare_id, id_aviz)
        elif "Aviz EE Delgaz" in avizCU.nume_aviz.nume:
            return common.aviz_EE_Delgaz(lucrare_id, id_aviz)
        elif "Aviz GN Delgaz" in avizCU.nume_aviz.nume:
            return common.aviz_GN_Delgaz(lucrare_id, id_aviz)
        elif "Aviz Orange" in avizCU.nume_aviz.nume:
            return common.aviz_Orange(lucrare_id, id_aviz)
        elif "Aviz Cultura" in avizCU.nume_aviz.nume:
            return common.aviz_Cultura(lucrare_id, id_aviz)

        # IASI
        elif lucrare.judet.nume == "Iași":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return common.aviz_APM(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = common.aviz_EE_delgaz(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație nu poate fi generată (...încă)")

        # NEAMȚ
        elif lucrare.judet.nume == "Neamț":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return common.aviz_APM(lucrare.id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = common.aviz_EE_delgaz_neamt(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Avizul nu poate fi generat - tipul avizului nu este valid")

        # BACĂU
        elif lucrare.judet.nume == "Bacău":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return common.aviz_APM(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = common.aviz_EE_delgaz_bacau(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Avizul nu poate fi generat - tipul avizului nu este valid")

            # SUCEAVA
        elif lucrare.judet.nume == "Suceava":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return common.aviz_APM(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = common.aviz_EE_delgaz(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Avizul nu poate fi generat - tipul avizului nu este valid")

        # BOTOȘANI
        elif lucrare.judet.nume == "Botoșani":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return common.aviz_APM(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = common.aviz_EE_delgaz(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Avizul nu poate fi generat - tipul avizului nu este valid")

        # VASLUI
        elif lucrare.judet.nume == "Vaslui":
            if avizCU.nume_aviz.nume == "Aviz APM":
                return common.aviz_APM(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = common.aviz_EE_delgaz(lucrare_id, id_aviz)

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
