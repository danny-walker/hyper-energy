from django.db import models


class WTManufacturer(models.Model):
    company = models.CharField(max_length=250, verbose_name="компания")
    country = models.CharField(max_length=250, verbose_name="страна")

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = "производитель ВЭУ"
        verbose_name_plural = "производители ВЭУ"


class WindTurbine(models.Model):
    manufacturer = models.ForeignKey(
        WTManufacturer, on_delete=models.CASCADE, verbose_name="производитель"
    )
    model_name = models.CharField(max_length=250, verbose_name="название модели")
    nominal_power = models.FloatField(
        max_length=250, verbose_name="номинальная мощность, кВт"
    )
    power_curve = models.JSONField(verbose_name="кривая мощности")

    def __str__(self):
        return self.model_name

    class Meta:
        verbose_name = "ветрогенератор"
        verbose_name_plural = "ветрогенераторы"


class WindParameter(models.Model):
    roughness_name = models.CharField(max_length=250, verbose_name="тип ландшафта")
    roughness = models.FloatField(
        max_length=250, verbose_name="значение шероховатости подстилающей поверхности"
    )

    def __str__(self):
        return self.roughness_name

    class Meta:
        verbose_name = "параметр ветра"
        verbose_name_plural = "параметры ветра"


class SMManufacturer(models.Model):
    company = models.CharField(max_length=250, verbose_name="производитель")
    country = models.CharField(max_length=250, verbose_name="страна")

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = "производитель СМ"
        verbose_name_plural = "производители СМ"


class SolarModule(models.Model):
    manufacturer = models.ForeignKey(
        SMManufacturer, on_delete=models.CASCADE, verbose_name="производитель"
    )
    model_name = models.CharField(max_length=250, verbose_name="название модели")
    nominal_power = models.FloatField(
        max_length=250, verbose_name="номинальная мощность, кВт"
    )
    sm_size = models.FloatField(max_length=250, verbose_name="площадь, м2")

    def __str__(self):
        return self.model_name

    class Meta:
        verbose_name = "солнечный модуль"
        verbose_name_plural = "солнечные модули"
