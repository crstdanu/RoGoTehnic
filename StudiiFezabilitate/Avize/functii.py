from StudiiFezabilitate.result import DocumentGenerationResult
import os
import shutil
import win32com.client as win32
import pythoncom
from docxtpl import DocxTemplate
import PyPDF2
from PyPDF2 import PdfMerger


pagina_goala = r"StudiiFezabilitate\Avize\modele_cereri\pagina_goala.pdf"


def check_required_fields(fields):
    for value, error_msg in fields:
        # Handle Django FileField objects
        from django.db.models.fields.files import FieldFile
        if isinstance(value, FieldFile):
            # If it's a file field, check if a file is associated with it
            if not value:
                return DocumentGenerationResult.error_result(error_msg)
        # Check for None or empty string (''), but allow zero values (0, 0.0)
        elif value is None or (isinstance(value, str) and value.strip() == ''):
            return DocumentGenerationResult.error_result(error_msg)
    return None


def copy_file(file_path, temp_dir, new_filename=None):
    """
    Copiază un fișier într-un director temporar și returnează calea completă a fișierului copiat.

    Args:
        file_path (str): Calea către fișierul original
        temp_dir (str): Directorul în care va fi copiat fișierul
        new_filename (str, optional): Numele nou al fișierului copiat. Dacă nu este specificat, se folosește numele original

    Returns:
        str: Calea completă a fișierului copiat

    Raises:
        ValueError: Dacă parametrii nu sunt valizi
        FileNotFoundError: Dacă fișierul sursă sau directorul destinație nu există
        PermissionError: Dacă nu există permisiuni pentru copiere
        Exception: Pentru alte erori în timpul copierii
    """
    try:
        # Verificăm dacă parametrii sunt valizi
        if not file_path or not isinstance(file_path, str):
            raise ValueError("Calea fișierului sursă nu este validă")

        if not temp_dir or not isinstance(temp_dir, str):
            raise ValueError("Directorul destinație nu este valid")

        # Curățăm path-ul de ghilimele
        file = file_path.strip('"')

        # Verificăm dacă fișierul sursă există
        if not os.path.exists(file):
            raise FileNotFoundError(f"Fișierul sursă nu a fost găsit: {file}")

        if os.path.getsize(file) == 0:
            print(f"Avertisment: Fișierul sursă este gol: {file}")

        # Verificăm dacă directorul destinație există
        if not os.path.exists(temp_dir):
            raise FileNotFoundError(
                f"Directorul destinație nu există: {temp_dir}")

        # Verificăm dacă avem permisiuni de scriere în directorul destinație
        if not os.access(temp_dir, os.W_OK):
            raise PermissionError(
                f"Nu există permisiuni de scriere în directorul destinație: {temp_dir}")

        # Construim calea de destinație și copiem fișierul
        if new_filename:
            # Dacă s-a specificat un nume nou, folosim extensia fișierului original
            original_extension = os.path.splitext(file)[1]
            if not new_filename.endswith(original_extension):
                new_filename += original_extension
            destination_path = os.path.join(temp_dir, new_filename)
        else:
            # Altfel, folosim numele original
            file_name = os.path.basename(file)
            destination_path = os.path.join(temp_dir, file_name)

        # Verificăm dacă fișierul există deja la destinație
        if os.path.exists(destination_path):
            print(
                f"Avertisment: Fișierul există deja la destinație și va fi suprascris: {destination_path}")

        shutil.copy(file, destination_path)

        # Verificăm dacă copierea a reușit
        if not os.path.exists(destination_path):
            raise Exception(
                f"Fișierul nu a fost copiat la destinație: {destination_path}")

        return destination_path
    except Exception as e:
        error_message = f"Eroare la copierea fișierului: {str(e)}"
        print(error_message)
        raise Exception(error_message)


def count_pages(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
    return num_pages


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
    word = None
    try:
        # Inițializăm COM pentru thread-ul curent
        pythoncom.CoInitialize()

        if not doc or not isinstance(doc, str):
            raise ValueError("Calea documentului nu este validă")

        if not os.path.exists(doc):
            raise FileNotFoundError(f"Documentul nu a fost găsit: {doc}")

        if not doc.lower().endswith('.docx'):
            raise ValueError(f"Fișierul trebuie să fie în format DOCX: {doc}")

        # Convertim calea la absolută pentru Word COM API
        doc = os.path.abspath(doc)

        # Gestionăm calea cu spații incluzând-o între ghilimele
        if ' ' in doc:
            doc_path_for_open = f'"{doc}"'
        else:
            doc_path_for_open = doc

        word = win32.DispatchEx("Word.Application")
        new_name = doc.replace(".docx", r".pdf")

        # Pentru siguranță, eliminăm ghilimelele din calea nouă pentru SaveAs
        new_name = new_name.strip('"')

        # Deschidem documentul Word
        worddoc = word.Documents.Open(doc_path_for_open)
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
            if doc and os.path.exists(doc):
                os.remove(doc)
                print(f"Fișierul temporar DOCX a fost șters: {doc}")
        except Exception as e:
            print(
                f"Nu s-a putut șterge fișierul DOCX: {doc}, eroare: {str(e)}")

        # Eliberăm resursele COM indiferent dacă funcția a reușit sau a eșuat
        try:
            pythoncom.CoUninitialize()
        except:
            pass


def create_document(model_path, context, final_destination, stampila=None, semnatura_1=None, semnatura_2=None):
    """
    Creează un document DOCX din șablon și îl convertește în PDF.

    Args:
        model_path (str): Calea către șablonul DOCX
        context (dict): Contextul pentru renderizarea șablonului
        final_destination (str): Directorul pentru documentul final
        stampila (str, optional): Calea către ștampilă
        semnatura_1 (str, optional): Calea către prima semnătură
        semnatura_2 (str, optional): Calea către a doua semnătură

    Returns:
        str: Calea către documentul PDF generat

    Raises:
        Exception: Dacă apare o eroare în timpul generării documentului
    """
    temp_files = []

    try:

        # Verificăm dacă directorul final există
        if not os.path.exists(final_destination):
            raise FileNotFoundError(
                f"Directorul destinație nu există: {final_destination}")

        # Verificăm existența ștampilelor/semnăturilor dacă sunt furnizate
        if stampila and not os.path.exists(stampila):
            raise FileNotFoundError(
                f":tampila nu a fost găsită: {stampila}")

        if semnatura_1 and not os.path.exists(semnatura_1):
            raise FileNotFoundError(
                f"Prima semnătură nu a fost găsită: {semnatura_1}")

        if semnatura_2 and not os.path.exists(semnatura_2):
            raise FileNotFoundError(
                f"A doua semnătură nu a fost găsită: {semnatura_2}")

        # Încărcăm șablonul
        try:
            doc = DocxTemplate(model_path)
        except Exception as e:
            raise Exception(f"Eroare la încărcarea șablonului: {str(e)}")

        # Înlocuim placeholder-urile pentru imagini
        try:
            if stampila:
                doc.replace_pic("Placeholder_1.png", stampila)

            if semnatura_1:
                doc.replace_pic("Placeholder_2.png", semnatura_1)

            if semnatura_2:
                doc.replace_pic("Placeholder_3.png", semnatura_2)
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


def copy_doc_to_pdf(model_path, final_destination):
    """
    Copiază un document DOCX și îl convertește în format PDF.

    Args:
        model_path (str): Calea către documentul DOCX sursă
        final_destination (str): Directorul destinație unde va fi copiat și convertit documentul

    Returns:
        str: Calea către documentul PDF generat

    Raises:
        ValueError: Dacă parametrii nu sunt valizi
        FileNotFoundError: Dacă documentul sursă sau directorul destinație nu există
        Exception: Pentru alte erori în timpul procesării documentului
    """
    try:
        # Verificăm dacă parametrii sunt valizi
        if not model_path or not isinstance(model_path, str):
            raise ValueError("Calea documentului sursă nu este validă")

        if not final_destination or not isinstance(final_destination, str):
            raise ValueError("Directorul destinație nu este valid")

        # Verificăm dacă documentul sursă există și este un fișier DOCX
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Documentul sursă nu a fost găsit: {model_path}")

        if not model_path.lower().endswith('.docx'):
            raise ValueError(
                f"Documentul sursă trebuie să fie în format DOCX: {model_path}")

        # Copiem documentul în directorul destinație
        path_doc = copy_file(model_path, final_destination)

        # Convertim documentul în PDF
        readme_pdf_path = convert_to_pdf(path_doc)

        # Verificăm dacă PDF-ul a fost generat cu succes
        if not os.path.exists(readme_pdf_path) or os.path.getsize(readme_pdf_path) == 0:
            raise Exception(
                f"PDF-ul a fost generat, dar fișierul este gol: {readme_pdf_path}")

        return readme_pdf_path

    except Exception as e:
        error_message = f"Eroare la copierea și conversia documentului: {str(e)}"
        print(error_message)
        raise Exception(error_message)


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


def merge_pdfs_print(pdf_list, output_path):
    """
    Combină mai multe fișiere PDF într-un singur document, adăugând o pagină goală 
    după fiecare PDF cu număr impar de pagini (util pentru imprimare față-verso).

    Args:
        pdf_list (list): Lista căilor către fișierele PDF de combinat
        output_path (str): Calea către fișierul PDF rezultat

    Returns:
        str: Calea către documentul PDF rezultat

    Raises:
        ValueError: Dacă lista de PDF-uri este invalidă sau goală
        FileNotFoundError: Dacă un fișier PDF sau directorul destinație nu există
        Exception: Pentru alte erori în timpul combinării PDF-urilor
    """
    try:
        # Verificăm dacă lista de PDF-uri este validă
        if not pdf_list or not isinstance(pdf_list, list):
            raise ValueError("Lista de fișiere PDF nu este validă")

        if len(pdf_list) == 0:
            raise ValueError("Lista de fișiere PDF este goală")

        # Verificăm existența paginii goale
        if not os.path.exists(pagina_goala):
            raise FileNotFoundError(
                f"Pagina goală nu a fost găsită: {pagina_goala}")

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
                x = count_pages(pdf)
                if x % 2 == 1:
                    merger.append(pagina_goala)
            except Exception as e:
                raise Exception(
                    f"Eroare la prelucrarea PDF-ului '{pdf}': {str(e)}")

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
        error_message = f"Eroare la combinarea PDF-urilor pentru imprimare: {str(e)}"
        print(error_message)
        raise Exception(error_message)


def multiply_by_3(value: int):
    """
    Înmulțește o valoare cu 3 și returnează rezultatul ca string cu două zecimale.

    Args:
        value (int): Valoarea care trebuie înmulțită cu 3

    Returns:
        str: Rezultatul înmulțirii, formatat ca string cu două zecimale
    """
    result = value * 3 if value else 0
    # Returnăm direct string-ul formatat cu 2 zecimale
    return f"{result:.2f}"
