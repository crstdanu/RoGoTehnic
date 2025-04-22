from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.services import avize as a
from StudiiFezabilitate.result import DocumentGenerationResult


def creeaza_fisier(lucrare_id, id_aviz):
    """
    Creează fișierele necesare pentru un aviz specific

    Args:
        lucrare_id: ID-ul lucrării
        id_aviz: ID-ul avizului

    Returns:
        DocumentGenerationResult: Rezultatul generării documentelor
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)

        if lucrare.judet.nume == "Iași":
            if avizCU.nume_aviz.nume == "Aviz APM":
                # Generăm avizul APM și emailul
                documentatie_APM = a.aviz_APM_iasi(lucrare_id, id_aviz)

                # Verificăm dacă documentația a fost generată cu succes
                if not isinstance(documentatie_APM, DocumentGenerationResult) or not documentatie_APM.is_success():
                    # Dacă documentația nu a fost generată cu succes, returnăm eroarea
                    if isinstance(documentatie_APM, DocumentGenerationResult):
                        return documentatie_APM
                    elif isinstance(documentatie_APM, str) and (documentatie_APM.startswith("Nu") or documentatie_APM.startswith("Avizul nu")):
                        return DocumentGenerationResult.error_result(documentatie_APM)
                    else:
                        return DocumentGenerationResult.error_result(
                            "Rezultat neașteptat de la generarea documentației avizului")

                # Acum generăm emailul
                email_APM = a.email_APM_iasi(lucrare_id, id_aviz)

                # Verificăm dacă emailul a fost generat cu succes
                if not isinstance(email_APM, DocumentGenerationResult) or not email_APM.is_success():
                    # Dacă emailul nu a fost generat cu succes, returnăm eroarea
                    if isinstance(email_APM, DocumentGenerationResult):
                        return email_APM
                    elif isinstance(email_APM, str) and (email_APM.startswith("Nu") or email_APM.startswith("Emailul nu")):
                        return DocumentGenerationResult.error_result(email_APM)
                    else:
                        return DocumentGenerationResult.error_result(
                            "Rezultat neașteptat de la generarea emailului")

                # Ambele au fost generate cu succes, creăm o listă cu ambele fișiere
                fisiere = []

                # Adăugăm documentația
                if isinstance(documentatie_APM, DocumentGenerationResult):
                    fisiere.extend(documentatie_APM.get_files())
                else:
                    # Compatibilitate cu versiunile vechi care returnează calea fișierului
                    fisiere.append(documentatie_APM)

                # Adăugăm emailul
                if isinstance(email_APM, DocumentGenerationResult):
                    fisiere.extend(email_APM.get_files())
                else:
                    # Compatibilitate cu versiunile vechi care returnează calea fișierului
                    fisiere.append(email_APM)

                # Returnăm un rezultat de succes cu toate fișierele
                return DocumentGenerationResult.success_result(fisiere)

            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
                output_path = a.aviz_EE_delgaz_iasi(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
            else:
                return DocumentGenerationResult.error_result(
                    "Avizul nu poate fi generat - tipul avizului APM nu este valid")
        elif lucrare.judet.nume == "Neamț":
            if avizCU.nume_aviz.nume == "Aviz APM":
                output_path = a.aviz_APM_neamt(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
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
                output_path = a.aviz_APM_bacau(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
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
                output_path = a.aviz_APM_suceava(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
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
                output_path = a.aviz_APM_botosani(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
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
                output_path = a.aviz_APM_vaslui(lucrare_id, id_aviz)

                # Verificăm dacă output_path este un mesaj de eroare
                if isinstance(output_path, str) and output_path.startswith("Nu") or output_path.startswith("Avizul nu"):
                    return DocumentGenerationResult.error_result(output_path)
                else:
                    return DocumentGenerationResult.success_result(output_path)
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
                "Avizul nu poate fi generat - judetul nu este valid")
    except Exception as e:
        # Captăm excepția și returnăm un rezultat de eroare
        return DocumentGenerationResult.error_result(f"Eroare la crearea fișierelor: {str(e)}")
