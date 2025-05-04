from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult
import StudiiFezabilitate.Avize.Common.functii as y
import StudiiFezabilitate.Avize.functii as x
import tempfile


def aviz_APM(lucrare_id, id_aviz):
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = y.verifica_campuri_necesare_APM(
            lucrare, firma, reprezentant, cu, beneficiar, contact)
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = y.genereaza_cerere_APM(
                lucrare, firma, reprezentant, beneficiar, contact, cu, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare notificare
            notificare_pdf_path = y.genereaza_notificare_APM(
                lucrare, firma, reprezentant, cu, beneficiar, contact, temp_dir)
            temp_files.append(notificare_pdf_path)

            if lucrare.judet.nume == "Bacău":
                # 4. Generare document final
                path_document_final = y.genereaza_document_final_APM_print(
                    lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir
                )
                fisiere_generate.append(path_document_final)

                # 5. Generare email
                email_pdf_path = y.genereaza_readme_APM_bacau(temp_dir)
                fisiere_generate.append(email_pdf_path)
            else:
                # 4. Generare document final
                path_document_final = y.genereaza_document_final_APM(
                    lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir
                )
                fisiere_generate.append(path_document_final)

                # 5. Generare email
                email_pdf_path = y.genereaza_email_APM(
                    lucrare, avizCU, beneficiar, cu, contact, temp_dir)
                fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            y.curata_fisierele_temporare(
                temp_files, path_document_final, fisiere_generate)
            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în aviz_APM: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_EE_Delgaz(lucrare_id, id_aviz):
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = y.verifica_campuri_necesare_EE_Delgaz(
            lucrare, firma, reprezentant, cu, beneficiar, contact)
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = y.genereaza_cerere_EE_Delgaz(
                lucrare, firma, reprezentant, beneficiar, contact, cu, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = y.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir
            )
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = y.genereaza_email_EE_Delgaz(
                lucrare, avizCU, beneficiar, cu, contact, temp_dir)
            fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            y.curata_fisierele_temporare(
                temp_files, path_document_final, fisiere_generate)
            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în aviz_EE_delgaz: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_GN_Delgaz(lucrare_id, id_aviz):
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = y.verifica_campuri_necesare_GN_Delgaz(
            lucrare, firma, reprezentant, cu, beneficiar, contact)
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = y.genereaza_cerere_GN_Delgaz(
                lucrare, firma, reprezentant, beneficiar, contact, cu, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = y.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir
            )
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = y.genereaza_email_GN_Delgaz(
                lucrare, avizCU, beneficiar, cu, contact, temp_dir)
            fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            y.curata_fisierele_temporare(
                temp_files, path_document_final, fisiere_generate)
            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în aviz_GN_delgaz: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Orange(lucrare_id, id_aviz):
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = y.verifica_campuri_necesare_Orange(
            firma, reprezentant, cu, beneficiar, contact)
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # În cazul avizului Orange, fișierele sunt copiate direct în temp_dir și adăugate
            # atât în temp_files (pentru curățarea în caz de eroare) cât și în fisiere_generate
            # (pentru a fi returnate utilizatorului)

            # 2. Generare cerere
            cerere_pdf_path = y.genereaza_cerere_Orange(
                firma, reprezentant, beneficiar, contact, cu, temp_dir)
            temp_files.append(cerere_pdf_path)
            fisiere_generate.append(cerere_pdf_path)

            # 3. Copie Certificatul de urbanism
            cu_path = x.copy_file(cu.cale_CU.path, temp_dir,
                                  "02. Certificat de urbanism")
            temp_files.append(cu_path)
            fisiere_generate.append(cu_path)

            # 4. Copie Plan incadrare CU
            plan_path = x.copy_file(
                cu.cale_plan_incadrare_CU.path, temp_dir, "03. Plan incadrare CU")
            temp_files.append(plan_path)
            fisiere_generate.append(plan_path)

            # 5. Copie Plan de situație CU
            plan_situatie_path = x.copy_file(
                cu.cale_plan_situatie_CU.path, temp_dir, "04. Plan de situație CU")
            temp_files.append(plan_situatie_path)
            fisiere_generate.append(plan_situatie_path)

            # 6. Copie Memoriul tehnic
            memoriu_tehnic_path = x.copy_file(
                cu.cale_memoriu_tehnic_CU.path, temp_dir, "05. Memoriu tehnic")
            temp_files.append(memoriu_tehnic_path)
            fisiere_generate.append(memoriu_tehnic_path)

            # 7. Copie Acte facturare
            acte_facturare_path = x.copy_file(
                cu.cale_acte_facturare.path, temp_dir, "06. Acte facturare")
            temp_files.append(acte_facturare_path)
            fisiere_generate.append(acte_facturare_path)

            # 8. Generare Readme
            readme_pdf_path = y.genereaza_readme_Orange(temp_dir)
            temp_files.append(readme_pdf_path)
            fisiere_generate.append(readme_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            y.curata_fisierele_temporare(
                temp_files, path_document_final, fisiere_generate)
            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în aviz_Orange: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Cultura(lucrare_id, id_aviz):
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = y.verifica_campuri_necesare_Cultura(
            lucrare, firma, reprezentant, cu, beneficiar, contact)
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = y.genereaza_cerere_Cultura(
                lucrare, firma, reprezentant, beneficiar, contact, cu, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = y.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir
            )
            fisiere_generate.append(path_document_final)

            if lucrare.judet.nume == "Iași" or lucrare.judet.nume == "Neamț":
                cerere_printabila_pdf_path = y.genereaza_document_final_print(
                    avizCU, cerere_pdf_path, cu, temp_dir)
                fisiere_generate.append(cerere_printabila_pdf_path)

            # 4. Generare email
            email_pdf_path = y.genereaza_email_Cultura(
                lucrare, avizCU, beneficiar, cu, contact, firma, temp_dir)
            fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            y.curata_fisierele_temporare(
                temp_files, path_document_final, fisiere_generate)
            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în aviz_Cultura: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")
