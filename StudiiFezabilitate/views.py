from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse

import os

from StudiiFezabilitate.models import Lucrare, CertificatUrbanism, AvizeCU
from StudiiFezabilitate.forms import LucrareForm, CertificatUrbanismForm, AvizeCUForm


# Create your views here.


def index(request):
    context = {
        'lucrari': Lucrare.objects.all(),
    }
    return render(request, 'StudiiFezabilitate/index.html', context)


def view_lucrare(request, id):
    lucrare = Lucrare.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))


def add(request):
    if request.method == 'POST':
        form = LucrareForm(request.POST)
        if form.is_valid():
            new_nume = form.cleaned_data['nume']
            new_nume_intern = form.cleaned_data['nume_intern']
            new_judet = form.cleaned_data['judet']
            new_localitate = form.cleaned_data['localitate']
            new_adresa = form.cleaned_data['adresa']
            new_firma_proiectare = form.cleaned_data['firma_proiectare']
            new_beneficiar = form.cleaned_data['beneficiar']
            new_lot = form.cleaned_data['lot']
            new_persoana_contact = form.cleaned_data['persoana_contact']
            new_finalizata = form.cleaned_data['finalizata']

            new_lucrare = Lucrare(
                nume=new_nume,
                nume_intern=new_nume_intern,
                judet=new_judet,
                localitate=new_localitate,
                adresa=new_adresa,
                firma_proiectare=new_firma_proiectare,
                beneficiar=new_beneficiar,
                lot=new_lot,
                persoana_contact=new_persoana_contact,
                finalizata=new_finalizata
            )

            new_lucrare.save()
            return render(request, 'StudiiFezabilitate/add.html', {
                'form': LucrareForm(),
                'success': True
            })
        else:
            return render(request, 'StudiiFezabilitate/add.html', {
                'form': form
            })
    else:
        form = LucrareForm()
    return render(request, 'StudiiFezabilitate/add.html', {
        'form': LucrareForm()
    })


def edit(request, id):
    if request.method == 'POST':
        lucrare = Lucrare.objects.get(pk=id)
        form = LucrareForm(request.POST, instance=lucrare)
        if form.is_valid():
            form.save()
            return render(request, 'StudiiFezabilitate/edit.html', {
                'form': form,  # LucrareForm(instance=lucrare)
                'success': True
            })
    else:
        lucrare = Lucrare.objects.get(pk=id)
        form = LucrareForm(instance=lucrare)
    return render(request, 'StudiiFezabilitate/edit.html', {
        'form': form
    })


def delete(request, id):
    if request.method == 'POST':
        lucrare = Lucrare.objects.get(pk=id)
        lucrare.delete()
    return HttpResponseRedirect(reverse('index'))


def index_CU(request, id):
    try:
        certificat_urbanism = CertificatUrbanism.objects.get(lucrare_id=id)
        avize = AvizeCU.objects.filter(certificat_urbanism=certificat_urbanism)
    except CertificatUrbanism.DoesNotExist:
        certificat_urbanism = None
        avize = []
    return render(request, 'CU/index.html', {
        'avize': avize,
        'certificat_urbanism': certificat_urbanism,
        'lucrare': Lucrare.objects.get(pk=id),
    })


def add_CU(request, id):
    lucrare = get_object_or_404(Lucrare, pk=id)
    if request.method == 'POST':
        form = CertificatUrbanismForm(request.POST, request.FILES)
        if form.is_valid():
            # Crează obiectul dar nu îl salvează încă
            certificat_urbanism = form.save(commit=False)
            certificat_urbanism.lucrare = lucrare  # Asignează lucrarea existentă
            certificat_urbanism.save()  # Salvează în baza de date

            return render(request, 'CU/add.html', {
                'form': CertificatUrbanismForm(),
                'success': True,
                'lucrare': lucrare
            })
        else:
            return render(request, 'CU/add.html', {
                'form': form,
                'lucrare': lucrare,
            })
    else:
        form = CertificatUrbanismForm()
    return render(request, 'CU/add.html', {
        'form': form,
        'lucrare': lucrare,
    })


def edit_CU(request, id):
    lucrare = get_object_or_404(Lucrare, pk=id)
    certificat_urbanism = CertificatUrbanism.objects.get(lucrare=lucrare)
    if request.method == 'POST':
        form = CertificatUrbanismForm(
            request.POST, request.FILES, instance=certificat_urbanism)
        if form.is_valid():
            form.save()
            return redirect('index_CU', id=lucrare.id)
        else:
            print(form.errors)
            return render(request, 'CU/edit.html', {
                'form': form,
                'lucrare': lucrare
            })

    else:
        form = CertificatUrbanismForm(instance=certificat_urbanism)
    return render(request, 'CU/edit.html', {
        'form': form,
        'lucrare': lucrare
    })


def add_Avize(request, id):
    lucrare = get_object_or_404(Lucrare, pk=id)
    certificat_urbanism = CertificatUrbanism.objects.get(lucrare=lucrare)
    if request.method == 'POST':
        form = AvizeCUForm(request.POST)
        if form.is_valid():
            aviz = form.save(commit=False)
            aviz.certificat_urbanism = certificat_urbanism
            aviz.save()
            return render(request, 'CU/add_avize.html', {
                'form': AvizeCUForm(),
                'success': True,
                'lucrare': lucrare
            })
        else:
            return render(request, 'CU/add_avize.html', {
                'form': form,
                'lucrare': lucrare
            })
    else:
        form = AvizeCUForm()

    return render(request, 'CU/add_avize.html', {
        'form': form,
        'lucrare': lucrare
    })


def edit_Aviz(request, lucrare_id, id):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    aviz = AvizeCU.objects.get(pk=id)
    if request.method == 'POST':
        form = AvizeCUForm(request.POST, instance=aviz)
        if form.is_valid():
            form.save()
            return render(request, 'CU/edit_avize.html', {
                'form': form,
                'success': True,
                'lucrare': lucrare,
                'aviz': aviz,
            })
    else:
        form = AvizeCUForm(instance=aviz)
    return render(request, 'CU/edit_avize.html', {
        'form': form,
        'lucrare': lucrare,
        'aviz': aviz,
    })


def delete_aviz(request, lucrare_id, id_aviz):
    if request.method == 'POST':
        aviz = AvizeCU.objects.get(pk=id_aviz)
        aviz.delete()

    return HttpResponseRedirect(reverse('index_CU', args=[lucrare_id]))


def download_file(request, model_name, field_name, object_id):
    """
    Descarcă oricare dintre câmpurile FileField din modelele specificate.

    Args:
        model_name: Numele modelului (ex: certificaturbanism)
        field_name: Numele câmpului de fișier (ex: cale_CU, cale_plan_incadrare_CU, etc.)
        object_id: ID-ul obiectului (pentru CertificatUrbanism este ID-ul lucrării)
    """
    try:
        # Importuri necesare
        import os
        from django.http import HttpResponse, Http404
        from django.shortcuts import get_object_or_404
        from StudiiFezabilitate.models import Lucrare, CertificatUrbanism

        # Determinăm modelul și obiectul în funcție de model_name
        if model_name.lower() == 'certificaturbanism':
            # Obținem obiectul
            lucrare = get_object_or_404(Lucrare, pk=object_id)
            obj = get_object_or_404(CertificatUrbanism, lucrare=lucrare)

            # Lista tuturor câmpurilor FileField din modelul CertificatUrbanism
            file_fields = [
                'cale_CU', 'cale_plan_incadrare_CU', 'cale_plan_situatie_CU',
                'cale_acte_beneficiar', 'cale_acte_facturare', 'cale_chitanta_APM',
                'cale_plan_situatie_la_scara', 'cale_plan_situatie_DWG', 'cale_extrase_CF',
                'cale_aviz_GIS', 'cale_ATR', 'cale_aviz_CTE', 'cale_chitanta_DSP'
            ]

            # Verificăm dacă câmpul specificat există în model
            if field_name not in file_fields:
                raise Http404(
                    f"Câmpul {field_name} nu există în modelul {model_name}")

            # Obținem câmpul și verificăm dacă există fișierul
            field = getattr(obj, field_name, None)
            if not field:
                raise Http404("Fișierul nu există")

            # Obținem calea fișierului și verificăm dacă există
            file_path = field.path
            if not os.path.exists(file_path):
                raise Http404("Fișierul nu există fizic pe server")

            # Determinăm tipul MIME corect în funcție de extensia fișierului
            content_type = 'application/octet-stream'  # Default
            extension = os.path.splitext(file_path)[1].lower()

            if extension == '.pdf':
                content_type = 'application/pdf'
            elif extension == '.dwg':
                content_type = 'application/acad'  # MIME type pentru fișiere AutoCAD

            # Deschidem fișierul și îl trimitem ca răspuns
            with open(file_path, 'rb') as f:
                response = HttpResponse(f, content_type=content_type)

                # Stabilim dacă fișierul va fi deschis în browser sau descărcat
                # PDF-urile pot fi afișate în browser, DWG-urile trebuie descărcate
                disposition = 'inline' if extension == '.pdf' else 'attachment'

                # Numele fișierului pentru descărcare
                filename = os.path.basename(file_path)
                response['Content-Disposition'] = f'{disposition}; filename="{filename}"'

                return response
        else:
            raise Http404(f"Modelul {model_name} nu este suportat")

    except Exception as e:
        # Pentru fiecare eroare, oferim un mesaj clar
        import sys
        error_type, error_value, error_traceback = sys.exc_info()
        error_message = f"Eroare: {error_type.__name__}: {error_value}"
        raise Http404(error_message)
