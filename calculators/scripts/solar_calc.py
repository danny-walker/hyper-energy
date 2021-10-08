from calculators.models import SolarModule

# Количество дней в месяцах
days_in_month = {
    "Jan": 31,
    "Feb": 28,
    "Mar": 31,
    "Apr": 30,
    "May": 31,
    "Jun": 30,
    "Jul": 31,
    "Aug": 31,
    "Sep": 30,
    "Oct": 31,
    "Nov": 30,
    "Dec": 31,
}

# Значения удельной солнечной инсоляции в день по месяцам по РБ, кВт*ч/м2
daily_solar_ins = {
    "Jan": 0.833,
    "Feb": 1.613,
    "Mar": 2.755,
    "Apr": 3.807,
    "May": 5.040,
    "Jun": 5.048,
    "Jul": 4.947,
    "Aug": 4.313,
    "Sep": 2.825,
    "Oct": 1.620,
    "Nov": 0.838,
    "Dec": 0.618,
}


def solar_data(model_name):
    # Определяем мощность СМ на основании данных выбора пользователя на frontend
    nominal_power = []
    queryset = SolarModule.objects.values_list("model_name", "nominal_power")
    for item in queryset:
        if str(model_name) == item[0]:
            nominal_power = item[1]
    return nominal_power


def output_power(power_cons, model_name):
    # daylight_hours — продолжительность светового дня. Это весьма условный параметр.
    # Надо понимать, что продолжительность светового дня — это не время от восхода Солнца до заката, а время
    # активной работы солнечной панели на максимальную мощность при высоких приходах солнечного излучения.
    # Зависит в основном от облачности и времени года. Варьируется в пределах от 1 до 10.
    daylight_hours = 5

    # k – коэффициент, равный 0,55 и 0,7 в летний и зимний периоды, соответственно.
    # Он делает поправку на потерю мощности солнечных элементов при нагреве на солнце, а также учитывает
    # наклонное падение лучей на поверхность модулей в течение дня.
    k_summer = 0.55
    k_winter = 0.7

    # Расчет значений солнечной инсоляции по месяцам и за год
    annual_solar_ins = []
    for value in days_in_month:
        month_solar_ins = days_in_month[value] * daily_solar_ins[value]
        annual_solar_ins.append(month_solar_ins)

    # # Коэффициент k_operating_mode характеризует отношение солнечной инсоляции при наименее солнечном месяца к
    # # радиации за # весь год. Если это отношение будет больше 50, то режим работы для СЭС необходимо выбрать
    # # сезонный, если меньше 50 – круглогодичный.
    # # Расчет коэффициента для определения режима работы СЭС
    # k_operating_mode = sum(annual_solar_ins) / min(annual_solar_ins)
    # if k_operating_mode >= 50:
    #     info_message = 'сезонный'
    # else:
    #     info_message = 'круглогодичный'

    # Выработка с одного СМ
    sm_power_output_annual_raw = []

    # Выработка с одного СМ за январь-март
    sm_power_output_jan_mar = [
        (k_winter * solar_data(model_name) * i / daylight_hours)
        for i in annual_solar_ins[:3]
    ]
    sm_power_output_annual_raw[:3] = sm_power_output_jan_mar

    # Добавляем выработку с одного СМ за апрель-август
    sm_power_output_apr_aug = [
        (k_summer * solar_data(model_name) * i / daylight_hours)
        for i in annual_solar_ins[3:9]
    ]
    sm_power_output_annual_raw[3:9] = sm_power_output_apr_aug

    # Добавляем выработку с одного СМ за октябрь-декабрь
    sm_power_output_oct_dec = [
        (k_winter * solar_data(model_name) * i / daylight_hours)
        for i in annual_solar_ins[9:]
    ]
    sm_power_output_annual_raw[9:] = sm_power_output_oct_dec

    # Средняя выработка за год
    sm_average_output = sum(sm_power_output_annual_raw) / len(
        sm_power_output_annual_raw
    )

    # Общая нагрузка + 20% на потери в инверторе, контроллере и пр.
    total_power_cons = 1.2 * power_cons

    # Количество солнечных модулей
    sm_quantity = int(round((total_power_cons / sm_average_output), 0))

    # Суммарная выработка с округлением
    spp_power_output_annual = [
        round((sm * sm_quantity), 2) for sm in sm_power_output_annual_raw
    ]
    spp_power_output = round((sum(spp_power_output_annual)), 2)

    # Возвращаем результаты расчета для отображения на frontend
    return {
        # 'info_message': info_message,
        "sm_quantity": sm_quantity,
        "spp_power_output_annual": spp_power_output_annual,
        "spp_power_output": spp_power_output,
    }
