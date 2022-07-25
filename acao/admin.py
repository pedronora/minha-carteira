from django.contrib import admin
from .models import Acao, Operacao


# Register your models here.
class FIIAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')


class OperacaoAdmin(admin.ModelAdmin):
    list_display = ('nr_nota', 'data', 'tipo', 'acao', 'preco',
                    'quantidade', 'custos', 'total_nota', 'user')


admin.site.register(Acao, FIIAdmin)
admin.site.register(Operacao, OperacaoAdmin)
