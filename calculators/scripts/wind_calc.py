import math
import numpy as np
from calculators.models import WindTurbine, WindParameter


# Достаем данные на основании выбора пользователя на frontend
def wind_data(model_name, roughness_length):
    # Данные ветрогенератора
    power_curve = []
    nominal_power = []
    queryset1 = WindTurbine.objects.values_list(
        "model_name", "power_curve", "nominal_power"
    )
    for item in queryset1:
        if str(model_name) == item[0]:
            power_curve = item[1]
            nominal_power = item[2]

    # Данные шероховатости подстилающей поверхности
    roughness = []
    queryset2 = WindParameter.objects.values_list("roughness_name", "roughness")
    for item in queryset2:
        if str(roughness_length) == item[0]:
            roughness = item[1]
    return [power_curve, nominal_power, roughness]


# Считаем выработку ВЭУ на основании данных ввода пользователя на frontend
def output_power(raw_wind_speed, meas_height, hub_height, roughness_length, model_name):
    # Пустой список для дифференциальной повторяемости
    diff_repeat_array = []

    # Ось скорости ветра для расчета дифференциальной повторяемости
    wind_speed_axis = range(1, 24)

    # Коэффициент пересчета скорости ветра с высоты ветроизмерений на высоту ВЭУ
    height_ratio_recount = math.log(
        hub_height / wind_data(model_name, roughness_length)[2]
    ) / math.log(meas_height / wind_data(model_name, roughness_length)[2])

    # Пересчет скорости ветра с высоты ветроизмерений на высоту ВЭУ
    wind_speed = raw_wind_speed * height_ratio_recount

    # Расчет среднеквадратического отклонения
    standard_deviation = math.sqrt(wind_speed)

    # Расчет коэффциента вариации
    variation_ratio = standard_deviation / wind_speed

    # Расчет коэффциента характеризующего форму кривой
    curve_shape_ratio = (0.9874 / variation_ratio) ** 1.0983

    # Расчет коэффциента характеризующего масштаб изменения функции распределения по оси скоростей
    scale_change_ratio = wind_speed * (0.568 + 0.434 / curve_shape_ratio) ** (
        -1 / curve_shape_ratio
    )

    # Расчет дифференциальной повторяемости
    for j in wind_speed_axis:
        diff_repeat = (
            curve_shape_ratio
            / scale_change_ratio
            * (j / scale_change_ratio) ** (curve_shape_ratio - 1)
            * math.exp((-1 * ((j / scale_change_ratio) ** curve_shape_ratio)))
        )
        diff_repeat_array.append(diff_repeat)
    diff_repeat_array_0 = 1 - math.fsum(diff_repeat_array)
    diff_repeat_array.insert(0, diff_repeat_array_0)

    # Расчет выработки для каждый градации скорости
    output_power_per_ms = (
        np.array(diff_repeat_array) * wind_data(model_name, roughness_length)[0]
    )
    # Расчет суммы выработки по всем градациям скорости
    output_power_sum = math.fsum(output_power_per_ms)

    # Расчет выработки энергии без учета потерь
    gross_production = round((output_power_sum * 8760 / 1000), 2)

    # Расчет КИУМ без учета потерь
    gross_capacity_factor = round(
        (output_power_sum * 100 / wind_data(model_name, roughness_length)[1]), 2
    )

    # Расчет выработки энергии с учетом потерь (потери приняты 15%)
    net_production = round((gross_production * (1 - 0.15)), 2)

    # Расчет КИУМ с учетом потерь (потери приняты 15%)
    net_capacity_factor = round(
        (
            net_production
            * 1000
            * 100
            / wind_data(model_name, roughness_length)[1]
            / 8760
        ),
        2,
    )

    # Возвращаем результаты расчета для отображения на frontend
    return {
        "gross_production": gross_production,
        "gross_capacity_factor": gross_capacity_factor,
        "net_production": net_production,
        "net_capacity_factor": net_capacity_factor,
        "wind_turbine": wind_data(model_name, roughness_length)[0],
    }
