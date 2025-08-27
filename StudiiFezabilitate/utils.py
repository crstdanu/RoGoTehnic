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
            if avizCU.nume_aviz.nume == "Aviz APM - Iasi":
                return iasi.aviz_APM_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz - Iasi":
                return iasi.aviz_EE_Delgaz_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz GN Delgaz - Iasi":
                return iasi.aviz_GN_Delgaz_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Orange - Iasi":
                return iasi.aviz_Orange_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Cultura - Iasi":
                return iasi.aviz_Cultura_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL":
                return iasi.aviz_HCL_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 2":
                return iasi.aviz_HCL_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 3":
                return iasi.aviz_HCL_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 4":
                return iasi.aviz_HCL_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 5":
                return iasi.aviz_HCL_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 6":
                return iasi.aviz_HCL_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 7":
                return iasi.aviz_HCL_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Apavital":
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
                return iasi.aviz_PMI_Spatii_Verzi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMI - Trafic urban":
                return iasi.aviz_PMI_Trafic_Urban(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMI - GIS Cadastru":
                return iasi.aviz_PMI_GIS(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMI - Nomenclatura urbana":
                return iasi.aviz_PMI_Nomenclatura_urbana(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Evidenta patrimoniu":
                return iasi.aviz_PMI_Evidenta_Patrimoniiu(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz DIGI - Iasi":
                return iasi.aviz_DIGI_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz MApN - Iasi":
                return iasi.aviz_MApN_Iasi(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz TransElectrica - Iasi":
                return iasi.aviz_TransElectrica_Iasi(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Iași nu poate fi generată (...încă)")

        # NEAMȚ
        elif lucrare.judet.nume == "Neamț":
            if avizCU.nume_aviz.nume == "Aviz APM - Neamt":
                return neamt.aviz_APM_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz - Neamt":
                return neamt.aviz_EE_Delgaz_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz GN Delgaz - Neamt":
                return neamt.aviz_GN_Delgaz_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Orange - Neamt":
                return neamt.aviz_Orange_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Cultura - Neamt":
                return neamt.aviz_Cultura_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL":
                return neamt.aviz_HCL_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 2":
                return neamt.aviz_HCL_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 3":
                return neamt.aviz_HCL_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 4":
                return neamt.aviz_HCL_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 5":
                return neamt.aviz_HCL_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 6":
                return neamt.aviz_HCL_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 7":
                return neamt.aviz_HCL_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz ApaServ":
                return neamt.aviz_ApaServ(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Luxten":
                return neamt.aviz_Luxten(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMPN Trafic":
                return neamt.aviz_PMPN_Trafic(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz PMPN Protocol HCL":
                return neamt.aviz_PMPN_Protocol_HCL(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Publiserv":
                return neamt.aviz_Publiserv(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz GN PrismaServ":
                return neamt.aviz_GN_PrismaServ(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Salubritate - Edil Industry":
                return neamt.aviz_Salubritate_Edil_Industry(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz DIGI - Neamt":
                return neamt.aviz_DIGI_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz MApN - Neamt":
                return neamt.aviz_MApN_Neamt(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz GN - Mihoc Oil SRL":
                return neamt.aviz_GN_Mihoc_Oil(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Neamț nu poate fi generată (...încă)")

        # BACĂU
        elif lucrare.judet.nume == "Bacău":
            if avizCU.nume_aviz.nume == "Aviz APM - Bacau":
                return bacau.aviz_APM_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz - Bacau":
                return bacau.aviz_EE_Delgaz_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz GN Delgaz - Bacau":
                return bacau.aviz_GN_Delgaz_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Orange - Bacau":
                return bacau.aviz_Orange_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL":
                return bacau.aviz_HCL_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 2":
                return bacau.aviz_HCL_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 3":
                return bacau.aviz_HCL_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 4":
                return bacau.aviz_HCL_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 5":
                return bacau.aviz_HCL_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 6":
                return bacau.aviz_HCL_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 7":
                return bacau.aviz_HCL_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz RAJA":
                return bacau.aviz_RAJA(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Romprest":
                return bacau.aviz_Romprest(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Acord Birou Tehnic Onesti":
                return bacau.acord_Birou_Tehnic_Onesti(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Acord Administrator Drum":
                return bacau.Acord_Administrator_Drum(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Apa CRAB":
                return bacau.aviz_Apa_CRAB(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz ChimComplex":
                return bacau.aviz_ChimComplex(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Drumuri Judetene Bacau":
                return bacau.aviz_Drumuri_Judetene_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz DIGI - Bacau":
                return bacau.aviz_DIGI_Bacau(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Salubritate SOMA":
                return bacau.aviz_Salubritate_SOMA(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz MApN - Bacau":
                return bacau.aviz_MApN_Bacau(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Bacău nu poate fi generată (...încă)")

            # SUCEAVA
        elif lucrare.judet.nume == "Suceava":
            if avizCU.nume_aviz.nume == "Aviz APM - Suceava":
                return suceava.aviz_APM_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz - Suceava":
                return suceava.aviz_EE_Delgaz_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz GN Delgaz - Suceava":
                return suceava.aviz_GN_Delgaz_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Orange - Suceava":
                return suceava.aviz_Orange_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL":
                return suceava.aviz_HCL_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 2":
                return suceava.aviz_HCL_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 3":
                return suceava.aviz_HCL_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 4":
                return suceava.aviz_HCL_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 5":
                return suceava.aviz_HCL_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 6":
                return suceava.aviz_HCL_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 7":
                return suceava.aviz_HCL_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz ACET":
                return suceava.aviz_ACET(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz GN NeoGas":
                return suceava.aviz_GN_NeoGas(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz DIGI - Suceava":
                return suceava.aviz_DIGI_Suceava(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz MApN - Suceava":
                return suceava.aviz_MApN_Suceava(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Suceava nu poate fi generată (...încă)")

        # BOTOȘANI
        elif lucrare.judet.nume == "Botoșani":
            if avizCU.nume_aviz.nume == "Aviz APM - Botosani":
                return botosani.aviz_APM_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz - Botosani":
                return botosani.aviz_EE_Delgaz_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz GN Delgaz - Botosani":
                return botosani.aviz_GN_Delgaz_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Orange - Botosani":
                return botosani.aviz_Orange_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Cultura - Botosani":
                return botosani.aviz_Cultura_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL":
                return botosani.aviz_HCL_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 2":
                return botosani.aviz_HCL_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 3":
                return botosani.aviz_HCL_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 4":
                return botosani.aviz_HCL_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 5":
                return botosani.aviz_HCL_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 6":
                return botosani.aviz_HCL_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 7":
                return botosani.aviz_HCL_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz NOVA ApaServ":
                return botosani.aviz_ApaServ(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz DIGI - Botosani":
                return botosani.aviz_DIGI_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz MApN - Botosani":
                return botosani.aviz_MApN_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Modern Calor SA":
                return botosani.aviz_Modern_Calor(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Acord CJ Botosani":
                return botosani.acord_CJ_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Acord Club Sportiv Botosani":
                return botosani.acord_Club_Sportiv_Botosani(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz principiu - Biroul Rutier - Botosani":
                return botosani.aviz_principiu_Biroul_Rutier_Botosani(lucrare_id, id_aviz)
            else:
                return DocumentGenerationResult.error_result(
                    "Aceasta documentație din Botoșani nu poate fi generată (...încă)")

        # VASLUI
        elif lucrare.judet.nume == "Vaslui":
            if avizCU.nume_aviz.nume == "Aviz APM - Vaslui":
                return vaslui.aviz_APM_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz EE Delgaz - Vaslui":
                return vaslui.aviz_EE_Delgaz_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz GN Delgaz - Vaslui":
                return vaslui.aviz_GN_Delgaz_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz Orange - Vaslui":
                return vaslui.aviz_Orange_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL":
                return vaslui.aviz_HCL_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 2":
                return vaslui.aviz_HCL_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 3":
                return vaslui.aviz_HCL_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 4":
                return vaslui.aviz_HCL_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 5":
                return vaslui.aviz_HCL_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 6":
                return vaslui.aviz_HCL_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz HCL - UAT 7":
                return vaslui.aviz_HCL_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz DIGI - Vaslui":
                return vaslui.aviz_DIGI_Vaslui(lucrare_id, id_aviz)
            elif avizCU.nume_aviz.nume == "Aviz MApN - Vaslui":
                return vaslui.aviz_MApN_Vaslui(lucrare_id, id_aviz)
            return DocumentGenerationResult.error_result(
                "Aceasta documentație din Vaslui nu poate fi generată (...încă)")
        else:
            return DocumentGenerationResult.error_result(
                "Documentația nu poate fi generată - nu am documentatii pentru avize din județul lucrării")
    except Exception as e:
        # Captăm excepția și returnăm un rezultat de eroare
        return DocumentGenerationResult.error_result(f"Eroare la crearea fișierelor: {str(e)}")
