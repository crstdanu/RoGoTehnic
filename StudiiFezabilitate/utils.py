from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.Avize.Common import avize as common
from StudiiFezabilitate.Avize.Iasi import avize as iasi
from StudiiFezabilitate.Avize.Neamt import avize as neamt
from StudiiFezabilitate.Avize.Bacau import avize as bacau
from StudiiFezabilitate.Avize.Botosani import avize as botosani
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
            if avizCU.nume_aviz.nume == "Aviz Apavital":
                return iasi.aviz_Apavital(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz GN Gazmir":
                return iasi.aviz_GN_Gazmir(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Termoficare":
                return iasi.aviz_Termoficare(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz CTP":
                return iasi.aviz_CTP(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Salubris":
                return iasi.aviz_Salubris(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMI - Mediu":
                return iasi.aviz_PMI_Mediu(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMI - Strazi municipale":
                return iasi.aviz_PMI_BSM(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMI - Utilitati publice":
                return iasi.aviz_PMI_SUP(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMI - Spatii verzi":
                return iasi.aviz_PMI_Spatii_verzi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMI - Trafic urban":
                return iasi.aviz_PMI_Trafic_urban(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMI - GIS Cadastru":
                return iasi.aviz_PMI_GIS_Cadastru(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMI - Nomenclatura urbana":
                return iasi.aviz_PMI_Nomenclatura_urbana(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Evidenta patrimoniu":
                return iasi.aviz_Evidenta_patrimoniu(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Iași nu poate fi generată (...încă)")

        # NEAMȚ
        elif lucrare.judet.nume == "Neamț":
            if avizCU.nume_aviz.nume == "Aviz ApaServ":
                return neamt.aviz_ApaServ(lucrare.id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Luxten":
                return neamt.aviz_Luxten(lucrare.id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMPN Trafic":
                return neamt.aviz_PMPN_Trafic(lucrare.id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMPN Protocol HCL":
                return neamt.aviz_PMPN_Protocol_HCL(lucrare.id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Publiserv":
                return neamt.aviz_Publiserv(lucrare.id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz GN PrismaServ":
                return neamt.aviz_GN_PrismaServ(lucrare.id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Salubritate - Edil Industry":
                return neamt.aviz_Salubritate_EdilIndustry(lucrare.id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Neamț nu poate fi generată (...încă)")

        # BACĂU
        elif lucrare.judet.nume == "Bacău":
            if avizCU.nume_aviz.nume == "Aviz RAJA":
                return bacau.aviz_RAJA(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Romprest":
                return bacau.aviz_Romprest(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Acord Birou Tehnic Onesti":
                return bacau.acord_Birou_Tehnic_Onesti(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Acord Administrator Drum":
                return bacau.acord_administrator_drum(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Apa CRAB":
                return bacau.aviz_Apa_CRAB(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz ChimComplex":
                return bacau.aviz_Chimcomplex(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Drumuri Judetene Bacau":
                return bacau.aviz_Drumuri_Judetene_Bacau(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Bacău nu poate fi generată (...încă)")

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
            if avizCU.nume_aviz.nume == "Aviz ApaServ":
                return botosani.aviz_ApaServ(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Botoșani nu poate fi generată (...încă)")

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
