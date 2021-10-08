from django.contrib import admin

from .models import (
    WTManufacturer,
    WindTurbine,
    SMManufacturer,
    SolarModule,
    WindParameter,
)


class WTManufacturerAdmin(admin.ModelAdmin):
    list_display = ("company", "country")
    list_filter = ("country",)
    search_fields = ("company", "country")


admin.site.register(WTManufacturer, WTManufacturerAdmin)


class WindTurbineAdmin(admin.ModelAdmin):
    list_display = ("manufacturer", "model_name", "nominal_power", "power_curve")
    list_filter = ("manufacturer", "nominal_power")
    search_fields = ("manufacturer", "nominal_power")


admin.site.register(WindTurbine, WindTurbineAdmin)


class WindParameterAdmin(admin.ModelAdmin):
    list_display = ("roughness_name", "roughness")
    search_fields = ("roughness_name",)


admin.site.register(WindParameter, WindParameterAdmin)


class SMManufacturerAdmin(admin.ModelAdmin):
    list_display = ("company", "country")
    list_filter = ("country",)
    search_fields = ("company", "country")


admin.site.register(SMManufacturer, SMManufacturerAdmin)


class SolarModuleAdmin(admin.ModelAdmin):
    list_display = ("manufacturer", "model_name", "nominal_power", "sm_size")
    list_filter = ("manufacturer", "nominal_power")
    search_fields = ("manufacturer", "nominal_power")


admin.site.register(SolarModule, SolarModuleAdmin)
