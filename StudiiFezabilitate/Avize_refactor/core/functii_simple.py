from StudiiFezabilitate.result import DocumentGenerationResult
from . import functii_baza as baza

import os
from datetime import datetime


# Functii de verificare

def verifica_campuri_APM(lucrare, firma, reprezentant, cu, beneficiar, contact):
    errors = baza.check_required_fields([
        (firma.nume, "Nu se poate genera avizul - lipsește numele firmei de proiectare"),
        (firma.adresa, "Nu se poate genera avizul - lipsește Adresa firmei de proiectare"),
        (firma.localitate, "Nu se poate genera avizul - lipsește Localitatea firmei de proiectare"),
        (firma.judet, "Nu se poate genera avizul - lipsește Județul firmei de proiectare"),
        (firma.email, "Nu se poate genera avizul - lipsește Email-ul firmei de proiectare"),

        (reprezentant.nume,
         "Nu se poate genera avizul - lipsește Reprezentantul firmei de proiectare"),

        (beneficiar.nume, "Nu se poate genera avizul - lipsește numele beneficiarului"),
        (beneficiar.localitate,
         "Nu se poate genera avizul - lipsește Localitatea beneficiarului"),
        (beneficiar.adresa, "Nu se poate genera avizul - lipsește Adresa beneficiarului"),
        (beneficiar.judet, "Nu se poate genera avizul - lipsește Județul beneficiarului"),

        (contact.nume, "Nu se poate genera avizul - lipsește Persoana de contact"),
        (contact.telefon, "Nu se poate genera avizul - lipsește Telefonul persoanei de contact"),

        (cu.nume, "Nu se poate genera avizul - lipsește Numele lucrarii din Certificatul de urbanism"),
        (cu.adresa, "Nu se poate genera avizul - lipsește Adresa lucrarii din Certificatul de urbanism"),
        (cu.descrierea_proiectului,
         "Nu se poate genera avizul - lipsește DESCRIEREA PROIECTULUI"),
        (cu.suprafata_ocupata,
         "Nu se poate genera avizul - lipsește SUPRAFAȚA LUCRĂRII din Certificatul de urbanism"),
    ])
    return errors


def verifica_fisiere_incarcate_APM(cu, firma, reprezentant):
    errors = baza.check_required_fields([
        # Fisiere necesare intocmire documentatie
        (firma.cale_stampila,
         "Nu se poate genera avizul - lipsește ștampila firmei de proiectare"),
        (reprezentant.cale_semnatura,
            "Nu se poate genera avizul - lipsește Semnatura reprezentantului firmei de proiectare"),
        (cu.inginer_intocmit.cale_semnatura,
            "Nu se poate genera avizul - lipsește Semnatura inginerului intocmit"),
        (cu.inginer_verificat.cale_semnatura,
            "Nu se poate genera avizul - lipsește Semnatura inginerului verificator"),

        # Fisiere necesare
        (cu.cale_CU,
         "Nu se poate genera avizul - lipsește Certificatul de Urbanism"),
        (cu.cale_plan_incadrare_CU,
            "Nu se poate genera avizul - lipsește Planul de incadrare in zona anexă CU"),
        (cu.cale_plan_situatie_CU,
            "Nu se poate genera avizul - lipsește Planul de situatie anexă CU"),
        (cu.cale_memoriu_tehnic_CU,
            "Nu se poate genera avizul - lipsește Memoriul tehnic anexă CU"),
        (cu.cale_acte_facturare,
            "Nu se poate genera avizul - lipsesc Acte facturare"),
        (cu.cale_chitanta_APM,
            "Nu se poate genera avizul - lipseste CHITANTA APM"),
    ])
    return errors


def verifica_existenta_modele(model_cerere, model_detalii, model_notificare=None):
    if not os.path.exists(model_cerere):
        return DocumentGenerationResult.error_result(
            "Nu găsesc modelul pentru Cerere")

    if model_notificare and not os.path.exists(model_notificare):
        return DocumentGenerationResult.error_result(
            "Nu găsesc modelul pentru Notificare")

    if not os.path.exists(model_detalii):
        return DocumentGenerationResult.error_result(
            "Nu găsesc șablonul pentru Detalii -> MODEL EMAIL sau Citeste-mă")

    return None  # No errors found


# Functii de generare documente
def genereaza_cerere_minimala(lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir):
    """
    Generează cererea pentru Aviz folosind date minimale
    și returnează calea către documentul generat.
    """

    context_cerere = {
        'nume_firma_': firma.nume,
        'localitate_firma': (firma.localitate.tip + ' ' + firma.localitate.nume).strip() if firma.localitate.tip else firma.localitate.nume,
        'adresa_firma': firma.adresa,
        'judet_firma': firma.judet.nume,
        'email_firma': firma.email,

        'nume_beneficiar': beneficiar.nume,

        'telefon_contact': contact.telefon,
        'persoana_contact': contact.nume,

        'nume_lucrare_CU': cu.nume,
        'adresa_lucrare_CU': cu.adresa,

        'data': datetime.now().strftime("%d.%m.%Y"), }

    # Generăm documentul și verificăm rezultatul
    cerere_pdf_path = baza.create_document(
        model_cerere,
        context_cerere,
        temp_dir,
        firma.cale_stampila.path,
        reprezentant.cale_semnatura.path,)

    return cerere_pdf_path


def genereaza_notificare_APM(lucrare, firma, reprezentant, cu, beneficiar, contact, model_notificare, temp_dir):
    """
    Generează notificarea pentru APM folosind datele furnizate
    și returnează calea către documentul generat.
    """

    context_notificare = {
        'nume_firma_': firma.nume,
        'localitate_firma': (firma.localitate.tip + ' ' + firma.localitate.nume).strip() if firma.localitate.tip else firma.localitate.nume,
        'adresa_firma': firma.adresa,
        'judet_firma': firma.judet.nume,
        'email_firma': firma.email,

        'reprezentant_firma': reprezentant.nume,


        'nume_lucrare_CU': cu.nume,
        'adresa_lucrare_CU': cu.adresa,

        'nume_beneficiar': beneficiar.nume,
        'localitate_beneficiar': (beneficiar.localitate.tip + ' ' + beneficiar.localitate.nume).strip() if beneficiar.localitate.tip else beneficiar.localitate.nume,
        'adresa_beneficiar': beneficiar.adresa,
        'judet_beneficiar': beneficiar.judet.nume,

        'suprafata_mp': cu.suprafata_ocupata,

        'descrierea_proiectului': cu.descrierea_proiectului,

        'inginer_intocmit': cu.inginer_intocmit.nume,
        'inginer_verificat': cu.inginer_verificat.nume,
    }

    notificare_pdf_path = baza.create_document(
        model_notificare, context_notificare, temp_dir,
        firma.cale_stampila.path,
        cu.inginer_intocmit.cale_semnatura.path,
        cu.inginer_verificat.cale_semnatura.path,
    )
    return notificare_pdf_path


# Aici se genereaza documentlele finale
def genereaza_document_final_APM(lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """
    path_document_final = os.path.join(
        temp_dir, f"Documentatie Aviz APM {lucrare.judet.nume} - {beneficiar.nume}.pdf"
    )

    pdf_list = [
        cerere_pdf_path,
        cu.cale_chitanta_APM.path,
        cu.cale_CU.path,
        cu.cale_plan_incadrare_CU.path,
        cu.cale_plan_situatie_CU.path,
        notificare_pdf_path,
        cu.cale_acte_facturare.path,
    ]

    baza.merge_pdfs(pdf_list, path_document_final)

    return path_document_final


# Aici se genereaza email si readme

def genereaza_email(lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir):
    """
    Generează emailul pentru APM și îl pregătește pentru a fi livrat
    """

    context_email = {
        'email': avizCU.nume_aviz.email,
        'nume_beneficiar': beneficiar.nume,
        'nr_cu': cu.numar,
        'data_cu': cu.data,
        'emitent_cu': cu.emitent,
        'nume_lucrare_CU': cu.nume,
        'adresa_lucrare_CU': cu.adresa,
        'persoana_contact': contact.nume,
        'telefon_contact': contact.telefon,
    }

    email_pdf_path = baza.create_document(
        model_detalii, context_email, temp_dir,
    )

    # Verifică dacă PDF-ul emailului există și are conținut
    if not os.path.exists(email_pdf_path) or os.path.getsize(email_pdf_path) == 0:
        raise Exception(
            f"Emailul a fost generat, dar fișierul este gol: {email_pdf_path}")

    return email_pdf_path
