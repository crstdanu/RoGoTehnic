from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.services import avize as a


def creeaza_fisier(lucrare_id, id_aviz):
    lucrare = Lucrare.objects.get(pk=lucrare_id)
    avizCU = AvizeCU.objects.get(pk=id_aviz)

    if lucrare.judet.nume == "Iași":
        if avizCU.nume_aviz.nume == "Aviz APM Iași":
            output_path = a.aviz_APM_iasi(lucrare_id, id_aviz)
            return output_path
        elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
            output_path = a.aviz_EE_delgaz_iasi(lucrare_id, id_aviz)
            return output_path
        else:
            return "Avizul nu poate fi generat - tipul avizului APM nu este valid"
    elif lucrare.judet.nume == "Neamț":
        if avizCU.nume_aviz.nume == "Aviz APM Neamț":
            output_path = a.aviz_APM_neamt(lucrare_id, id_aviz)
            return output_path
        elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
            output_path = a.aviz_EE_delgaz_neamt(lucrare_id, id_aviz)
            return output_path
        else:
            return "Avizul nu poate fi generat - tipul avizului nu este valid"
    elif lucrare.judet.nume == "Bacău":
        if avizCU.nume_aviz.nume == "Aviz APM Bacău":
            output_path = a.aviz_APM_bacau(lucrare_id, id_aviz)
            return output_path
        elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
            output_path = a.aviz_EE_delgaz_bacau(lucrare_id, id_aviz)
            return output_path
        else:
            return "Avizul nu poate fi generat - tipul avizului nu este valid"
    elif lucrare.judet.nume == "Suceava":
        if avizCU.nume_aviz.nume == "Aviz APM Suceava":
            output_path = a.aviz_APM_suceava(lucrare_id, id_aviz)
            return output_path
        elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
            output_path = a.aviz_EE_delgaz_suceava(lucrare_id, id_aviz)
            return output_path
        else:
            return "Avizul nu poate fi generat - tipul avizului nu este valid"
    elif lucrare.judet.nume == "Botoșani":
        if avizCU.nume_aviz.nume == "Aviz APM Botoșani":
            output_path = a.aviz_APM_botosani(lucrare_id, id_aviz)
            return output_path
        elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
            output_path = a.aviz_EE_delgaz_botosani(lucrare_id, id_aviz)
            return output_path
        else:
            return "Avizul nu poate fi generat - tipul avizului nu este valid"
    elif lucrare.judet.nume == "Vaslui":
        if avizCU.nume_aviz.nume == "Aviz APM Vaslui":
            output_path = a.aviz_APM_vaslui(lucrare_id, id_aviz)
            return output_path
        elif avizCU.nume_aviz.nume == "Aviz EE Delgaz":
            output_path = a.aviz_EE_delgaz_vaslui(lucrare_id, id_aviz)
            return output_path
        else:
            return "Avizul nu poate fi generat - tipul avizului nu este valid"
    else:
        return "Avizul nu poate fi generat - judetul nu este valid"
