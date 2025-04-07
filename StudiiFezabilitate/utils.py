from StudiiFezabilitate.models import AvizeCU, Lucrare


def aviz_APM_iasi(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    aviz = AvizeCU.objects.get(pk=id)
    pass
