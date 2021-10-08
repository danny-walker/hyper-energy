def output_power(daily_gas_volume):
    # Тепловая мощность биогазового комплекса на базе ДВС, кВт
    thermal_power = round(((daily_gas_volume * 5200 * 52 * 1.163) / (24 * 10 ** 5)), 2)

    # Отпуск тепловой энергии в год, Гкал/год
    thermal_prod = round(
        ((thermal_power * 8350 - (daily_gas_volume * 1.49 * 8760) / 24) / 1163), 2
    )

    # Электрическая мощность биогазового комплекса на базе ДВС, кВт
    electric_power = round(((daily_gas_volume * 5200 * 35 * 1.163) / (24 * 10 ** 5)), 2)

    # Отпуск электрической энергии в год, кВт*ч/год
    electricity_prod = round(
        (electric_power * 8350 - daily_gas_volume * 1.49 * 8760 / 24), 2
    )

    # Возвращаем результаты расчета для отображения на frontend
    return {
        "thermal_power": thermal_power,
        "thermal_prod": thermal_prod,
        "electric_power": electric_power,
        "electricity_prod": electricity_prod,
    }
