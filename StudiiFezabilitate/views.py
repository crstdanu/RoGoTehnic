from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from StudiiFezabilitate.models import Lucrare, CertificatUrbanism, AvizeCU
from StudiiFezabilitate.forms import LucrareForm

# Create your views here.


def index(request):
    return render(request, 'StudiiFezabilitate/index.html', {'lucrari': Lucrare.objects.all()})


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


def view_CU(request, id):
    try:
        certificat_urbanism = CertificatUrbanism.objects.get(lucrare_id=id)
        avize = AvizeCU.objects.filter(certificat_urbanism=certificat_urbanism)
    except CertificatUrbanism.DoesNotExist:
        certificat_urbanism = None
        avize = []
    return render(request, 'CU/index.html', {
        'avize': avize,
        'certificat_urbanism': certificat_urbanism
    })
