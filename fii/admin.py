from django.contrib import admin
from .models import FII, Operacao


# Register your models here.
class FIIAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo')


class OperacaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'nr_nota', 'tipo', 'fii', 'preco',
                    'quantidade', 'custos', 'nota_total')


admin.site.register(FII, FIIAdmin)
admin.site.register(Operacao, OperacaoAdmin)
