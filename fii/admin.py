from django.contrib import admin
from .models import FII, Operacao


# Register your models here.
class FIIAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')


class OperacaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'nr_nota', 'tipo', 'fii', 'preco',
                    'quantidade', 'custos', 'total_nota')


admin.site.register(FII, FIIAdmin)
admin.site.register(Operacao, OperacaoAdmin)
