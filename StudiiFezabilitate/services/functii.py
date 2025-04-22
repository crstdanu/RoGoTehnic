from StudiiFezabilitate.result import DocumentGenerationResult
import os
import win32com.client as win32
import pythoncom
from docxtpl import DocxTemplate
from PyPDF2 import PdfMerger


def check_required_fields(fields):
    for value, error_msg in fields:
        if not value:
            return DocumentGenerationResult.error_result(error_msg)
    return None


def convert_to_pdf(doc):
    """
    Convertește un document DOCX în PDF folosind Microsoft Word.
    Șterge fișierul DOCX după conversie, indiferent de rezultat.

    Args:
        doc (str): Calea către documentul DOCX

    Returns:
        str: Calea către documentul PDF generat

    Raises:
        Exception: Dacă apare o eroare în timpul conversiei
    """
    # Inițializăm COM pentru thread-ul curent
    pythoncom.CoInitialize()

    if not doc or not isinstance(doc, str):
        raise ValueError("Calea documentului nu este validă")

    if not os.path.exists(doc):
        raise FileNotFoundError(f"Documentul nu a fost găsit: {doc}")

    if not doc.lower().endswith('.docx'):
        raise ValueError(f"Fișierul trebuie să fie în format DOCX: {doc}")

    word = None
    try:
        word = win32.DispatchEx("Word.Application")
        new_name = doc.replace(".docx", r".pdf")
        worddoc = word.Documents.Open(doc)
        worddoc.SaveAs(new_name, FileFormat=17)
        worddoc.Close()

        if not os.path.exists(new_name) or os.path.getsize(new_name) == 0:
            raise Exception(
                f"PDF-ul a fost generat, dar fișierul este gol: {new_name}")

        return new_name
    except pythoncom.com_error as e:
        error_message = f"Eroare COM în timpul conversiei: {str(e)}"
        print(error_message)
        raise Exception(error_message)
    except Exception as e:
        error_message = f"Eroare la convertirea documentului în PDF: {str(e)}"
        print(error_message)
        raise Exception(error_message)
    finally:
        # Încercăm să închidem Word dacă instanța există
        if word:
            try:
                word.Quit()
            except:
                pass

        # Ștergem fișierul DOCX indiferent de rezultat
        try:
            if os.path.exists(doc):
                os.remove(doc)
                print(f"Fișierul temporar DOCX a fost șters: {doc}")
        except Exception as e:
            print(
                f"Nu s-a putut șterge fișierul DOCX: {doc}, eroare: {str(e)}")

        # Eliberăm resursele COM indiferent dacă funcția a reușit sau a eșuat
        pythoncom.CoUninitialize()


def create_document(model_path, context, final_destination, stampila_1=None, stampila_2=None, stampila_3=None):
    """
    Creează un document DOCX din șablon și îl convertește în PDF.

    Args:
        model_path (str): Calea către șablonul DOCX
        context (dict): Contextul pentru renderizarea șablonului
        final_destination (str): Directorul pentru documentul final
        stampila_1 (str, optional): Calea către prima ștampilă/semnătură
        stampila_2 (str, optional): Calea către a doua ștampilă/semnătură
        stampila_3 (str, optional): Calea către a treia ștampilă/semnătură

    Returns:
        str: Calea către documentul PDF generat

    Raises:
        Exception: Dacă apare o eroare în timpul generării documentului
    """
    temp_files = []

    try:
        # Verificăm existența șablonului
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Șablonul nu a fost găsit: {model_path}")

        # Verificăm dacă directorul final există
        if not os.path.exists(final_destination):
            raise FileNotFoundError(
                f"Directorul destinație nu există: {final_destination}")

        # Verificăm existența ștampilelor/semnăturilor dacă sunt furnizate
        if stampila_1 and not os.path.exists(stampila_1):
            raise FileNotFoundError(
                f"Prima ștampilă/semnătură nu a fost găsită: {stampila_1}")

        if stampila_2 and not os.path.exists(stampila_2):
            raise FileNotFoundError(
                f"A doua ștampilă/semnătură nu a fost găsită: {stampila_2}")

        if stampila_3 and not os.path.exists(stampila_3):
            raise FileNotFoundError(
                f"A treia ștampilă/semnătură nu a fost găsită: {stampila_3}")

        # Încărcăm șablonul
        try:
            doc = DocxTemplate(model_path)
        except Exception as e:
            raise Exception(f"Eroare la încărcarea șablonului: {str(e)}")

        # Înlocuim placeholder-urile pentru imagini
        try:
            if stampila_1:
                doc.replace_pic("Placeholder_1.png", stampila_1)

            if stampila_2:
                doc.replace_pic("Placeholder_2.png", stampila_2)

            if stampila_3:
                doc.replace_pic("Placeholder_3.png", stampila_3)
        except Exception as e:
            raise Exception(
                f"Eroare la înlocuirea imaginilor în șablon: {str(e)}")

        # Renderizăm contextul
        try:
            doc.render(context)
        except Exception as e:
            raise Exception(
                f"Eroare la popularea șablonului cu date: {str(e)}")

        # Salvăm documentul DOCX
        nume = os.path.basename(model_path).strip('.docx')
        path_doc = os.path.join(final_destination, f'{nume}.docx')

        try:
            doc.save(path_doc)
            temp_files.append(path_doc)
        except Exception as e:
            raise Exception(f"Eroare la salvarea documentului DOCX: {str(e)}")

        if not os.path.exists(path_doc) or os.path.getsize(path_doc) == 0:
            raise Exception(
                f"Documentul DOCX a fost generat, dar fișierul este gol: {path_doc}")

        # Convertim în PDF
        try:
            cerere_pdf_path = convert_to_pdf(path_doc)
            if not os.path.exists(cerere_pdf_path) or os.path.getsize(cerere_pdf_path) == 0:
                raise Exception(
                    f"PDF-ul a fost generat, dar fișierul este gol: {cerere_pdf_path}")
        except Exception as e:
            raise Exception(f"Eroare la convertirea în PDF: {str(e)}")

        return cerere_pdf_path
    except Exception as e:
        error_message = f"Eroare la crearea documentului: {str(e)}"
        print(error_message)
        raise Exception(error_message)
    finally:
        # Curățăm fișierele temporare
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    print(
                        f"Nu s-a putut șterge fișierul temporar: {temp_file}")


def merge_pdfs(pdf_list, output_path):
    """
    Combină mai multe fișiere PDF într-un singur document.

    Args:
        pdf_list (list): Lista căilor către fișierele PDF de combinat
        output_path (str): Calea către fișierul PDF rezultat

    Returns:
        str: Calea către documentul PDF rezultat

    Raises:
        Exception: Dacă apare o eroare în timpul combinării PDF-urilor
    """
    try:
        # Verificăm dacă lista de PDF-uri este validă
        if not pdf_list or not isinstance(pdf_list, list):
            raise ValueError("Lista de fișiere PDF nu este validă")

        if len(pdf_list) == 0:
            raise ValueError("Lista de fișiere PDF este goală")

        # Verificăm existența fiecărui PDF din listă
        for pdf in pdf_list:
            if not os.path.exists(pdf):
                raise FileNotFoundError(f"Fișierul PDF nu a fost găsit: {pdf}")

            if os.path.getsize(pdf) == 0:
                raise ValueError(f"Fișierul PDF este gol: {pdf}")

        # Verificăm dacă directorul de destinație există
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            raise FileNotFoundError(
                f"Directorul destinație nu există: {output_dir}")

        merger = PdfMerger()
        for pdf in pdf_list:
            try:
                merger.append(pdf)
            except Exception as e:
                raise Exception(
                    f"Eroare la adăugarea PDF-ului '{pdf}': {str(e)}")

        try:
            merger.write(output_path)
        except Exception as e:
            raise Exception(f"Eroare la scrierea PDF-ului combinat: {str(e)}")

        merger.close()

        # Verificăm dacă fișierul a fost creat cu succes
        if not os.path.exists(output_path):
            raise Exception(
                f"PDF-ul combinat nu a fost generat: {output_path}")

        if os.path.getsize(output_path) == 0:
            raise Exception(
                f"PDF-ul combinat a fost generat, dar fișierul este gol: {output_path}")

        return output_path
    except Exception as e:
        error_message = f"Eroare la combinarea PDF-urilor: {str(e)}"
        print(error_message)
        raise Exception(error_message)
