from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import ClientForm
from .models import Conso_eur, Conso_watt
from statistics import mean
from . import utils
from django.http import HttpResponse
import json

current_year = utils.current_year
previous_year = current_year -1 

class ClientFormView(View):
    def get(self, request):
        return render(request, 'dashboard/accueil.html')

    def post(self, request):
        form = ClientForm(request.POST)

        if form.is_valid():
            client_id = form.cleaned_data['client']
            return redirect('dashboard:results', client_id=client_id)

def annual_sum(conso):
    return sum([
            conso.janvier,
            conso.fevrier,
            conso.mars,
            conso.octobre,
            conso.avril,
            conso.mai,
            conso.juin,
            conso.juillet,
            conso.aout,
            conso.septembre,        
            conso.novembre,
            conso.decembre,])

def _average_winter_consumption(conso_watt):
    return mean([conso_watt.octobre,
                 conso_watt.novembre,
                 conso_watt.decembre,
                 conso_watt.janvier,
                 conso_watt.avril,
                 conso_watt.fevrier])

def _average_sommer_consumption(conso_watt):
    return mean([conso_watt.avril,
                 conso_watt.mai,
                 conso_watt.juin,
                 conso_watt.juillet,
                 conso_watt.aout,
                 conso_watt.septembre])

def _is_elec_heating(id):
    conso_watt = Conso_watt.objects.get(id=id)
    winter_sommer_ratio = _average_winter_consumption(conso_watt) / _average_sommer_consumption(conso_watt)
    if winter_sommer_ratio > utils.elec_heating_ratio:
        return True, winter_sommer_ratio
    return False, None

def _dysfunction_detected(conso_watt, conso_watt_previous_year):
    variance = abs((annual_sum(conso_watt) - annual_sum(conso_watt_previous_year)) / annual_sum(conso_watt_previous_year))
    if variance > utils.dysfunction_variance:
        return True, variance

    return False, None

def get_client_data(client_id):
    conso_euro = Conso_eur.objects.get(client_id=client_id, year=current_year)
    conso_euro_previous_year = Conso_eur.objects.get(client_id=client_id, year=previous_year)
    conso_watt = Conso_watt.objects.get(client_id=client_id, year=current_year)
    conso_watt_previous_year = Conso_watt.objects.get(client_id=client_id, year=previous_year)
    annual_costs = [
        int(annual_sum(conso_euro)),
        int(annual_sum(conso_euro_previous_year))]
    annual_consumption = {
        current_year: int(annual_sum(conso_watt)),
        (current_year-1): int(annual_sum(conso_watt_previous_year)),
    }

    data_conso = {
        'Janvier':  int(conso_watt.janvier),
        'Fevrier':  int(conso_watt.fevrier),
        'Mars':     int(conso_watt.mars),
        'Avril':    int(conso_watt.avril),
        'Mai':      int(conso_watt.mai),
        'Juin':     int(conso_watt.juin),
        'Juillet':  int(conso_watt.juillet),
        'Aout':     int(conso_watt.aout),
        'Septembre':int(conso_watt.septembre),
        'Octobre':  int(conso_watt.octobre),
        'Novembre': int(conso_watt.novembre),
        'Decembre': int(conso_watt.decembre),
    }
    return conso_euro, conso_watt, conso_euro_previous_year, conso_watt_previous_year, annual_costs, annual_consumption, data_conso


def results(request, client_id):
    is_elec_heating, winter_sommer_ratio = _is_elec_heating(client_id)
    conso_euro, conso_watt, conso_euro_previous_year, conso_watt_previous_year, annual_costs, annual_consumption, data_conso = get_client_data(client_id)
    dysfunction_detected, _ = _dysfunction_detected(conso_watt, conso_watt_previous_year)
    context = {
        "conso_euro": conso_euro,
        "conso_watt": conso_watt,
        "annual_costs": annual_costs,
        "annual_costs" : annual_costs,
        "annual_consumption": annual_consumption,
        "is_elec_heating": "Oui (Avez-vous pensé à l'auto-consommation ?)" if is_elec_heating else "Non (Saviez-vous qu'HelloWatt propose des contrats Gaz ?)",
        "dysfunction_detected": "Nous avons détecté une anomalie, votre conseiller HelloWatt vous contactera sous peu" if dysfunction_detected else "Néant",
        "winter_sommer_ratio": winter_sommer_ratio,
        "conso_watt_string": data_conso  
        }
    return render(request, 'dashboard/results.html', context)

def api(request, client_id):
    res = HttpResponse()
    res.status_code = 200
    res. content_type = "application/json"
    _, _, _, _, _, _, data_conso = get_client_data(client_id)
    res.content = json.dumps(data_conso, default=str)
    return res