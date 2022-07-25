from django.contrib import admin
from .models import Acao, Operacao


# Register your models here.
class FIIAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo')


class OperacaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'nr_nota', 'tipo', 'acao', 'preco',
                    'quantidade', 'custos', 'nota_total')


admin.site.register(Acao, FIIAdmin)
admin.site.register(Operacao, OperacaoAdmin)
