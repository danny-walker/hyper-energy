from django.shortcuts import render

from .forms import WindCalcForm, SolarCalcForm, BioCalcForm
from .scripts import wind_calc, solar_calc, bio_calc


def wind_calc_view(request):
    wind_data = {}
    if request.method == "POST":
        form = WindCalcForm(data=request.POST)
        if form.is_valid():
            raw_wind_speed = form.cleaned_data.get("raw_wind_speed")
            meas_height = form.cleaned_data.get("meas_height")
            roughness_length = form.cleaned_data.get("roughness_length")
            model_name = form.cleaned_data.get("model_name")
            hub_height = form.cleaned_data.get("hub_height")
            wind_data = wind_calc.output_power(
                raw_wind_speed, meas_height, hub_height, roughness_length, model_name
            )
    else:
        form = WindCalcForm()
    return render(
        request, "calculators/wind_calc.html", {"wind_data": wind_data, "form": form}
    )


def solar_calc_view(request):
    solar_data = {}
    if request.method == "POST":
        form = SolarCalcForm(request.POST)
        if form.is_valid():
            power_cons = form.cleaned_data.get("power_cons")
            model_name = form.cleaned_data.get("model_name")
            solar_data = solar_calc.output_power(power_cons, model_name)
    else:
        form = SolarCalcForm()
    return render(
        request, "calculators/solar_calc.html", {"solar_data": solar_data, "form": form}
    )


def bio_calc_view(request):
    bio_data = {}
    if request.method == "POST":
        form = BioCalcForm(request.POST)
        if form.is_valid():
            daily_gas_volume = form.cleaned_data.get("daily_gas_volume")
            bio_data = bio_calc.output_power(daily_gas_volume)
    else:
        form = BioCalcForm()
    return render(
        request, "calculators/bio_calc.html", {"bio_data": bio_data, "form": form}
    )
