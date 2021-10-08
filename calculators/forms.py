from django import forms
from crispy_forms.helper import FormHelper
from django_select2.forms import ModelSelect2Widget

from .models import (
    WindTurbine,
    WTManufacturer,
    WindParameter,
    SMManufacturer,
    SolarModule,
)


class WindCalcForm(forms.Form):
    raw_wind_speed = forms.FloatField()
    meas_height = forms.FloatField()
    hub_height = forms.FloatField()
    roughness_length = forms.ModelChoiceField(
        queryset=WindParameter.objects.all(), empty_label="Выберите тип ландшафта"
    )

    manufacturer = forms.ModelChoiceField(
        queryset=WTManufacturer.objects.all().order_by("company"),
        label=u"company",
        widget=ModelSelect2Widget(
            model=WTManufacturer,
            attrs={
                "data-minimum-input-length": 0,
                "data-placeholder": "Выберите производителя",
            },
            search_fields=["company__icontains"],
        ),
    )

    model_name = forms.ModelChoiceField(
        queryset=WindTurbine.objects.all().order_by("model_name"),
        label=u"model_name",
        widget=ModelSelect2Widget(
            model=WindTurbine,
            attrs={
                "data-minimum-input-length": 0,
                "data-placeholder": "Выберите модель",
            },
            search_fields=["model_name__icontains"],
            dependent_fields={"manufacturer": "manufacturer"},
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields["raw_wind_speed"].widget.attrs["min"] = 0.001
        self.fields["meas_height"].widget.attrs["min"] = 0.001
        self.fields["hub_height"].widget.attrs["min"] = 0.001


class SolarCalcForm(forms.Form):
    power_cons = forms.FloatField()

    manufacturer = forms.ModelChoiceField(
        queryset=SMManufacturer.objects.all().order_by("company"),
        label=u"company",
        widget=ModelSelect2Widget(
            model=SMManufacturer,
            attrs={
                "data-minimum-input-length": 0,
                "data-placeholder": "Выберите производителя",
            },
            search_fields=["company__icontains"],
        ),
    )

    model_name = forms.ModelChoiceField(
        queryset=SolarModule.objects.all().order_by("model_name"),
        label=u"model_name",
        widget=ModelSelect2Widget(
            model=SolarModule,
            attrs={
                "data-minimum-input-length": 0,
                "data-placeholder": "Выберите модель",
            },
            search_fields=["model_name__icontains"],
            dependent_fields={"manufacturer": "manufacturer"},
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class BioCalcForm(forms.Form):
    daily_gas_volume = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
