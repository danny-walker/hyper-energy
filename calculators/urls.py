from django.urls import path
from . import views


urlpatterns = [
    # Калькулятор ветрогенератора
    path("wind-calculator/", views.wind_calc_view, name="wind_calc_view"),
    # Калькулятор солнечной электростанции
    path("solar-calculator/", views.solar_calc_view, name="solar_calc_view"),
    # Калькулятор биогазового комплекса
    path("bio-calculator/", views.bio_calc_view, name="bio_calc_view"),
]
