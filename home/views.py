from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from acao.models import AcaoByUser, Operacao as Op_Acao
from fii.models import FIIByUser, Operacao as Op_Fii

# Create your views here.
class HomeView(TemplateView, LoginRequiredMixin):
    login_url = 'usuarios:entrar'
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' - Início'
        user = self.request.user
        context['acao_count'] = AcaoByUser.objects.filter(user=user).count()
        context['fii_count'] = FIIByUser.objects.filter(user=user).count()

        operacoes_fii = Op_Fii.objects.filter(user=user)
        operacoes_acao = Op_Acao.objects.filter(user=user)
        context['op_count'] = operacoes_fii.count() + operacoes_acao.count()
        total_soma_acao = operacoes_acao.last().soma_total if operacoes_acao else 0
        total_soma_fii = operacoes_fii.last().soma_total if operacoes_fii else 0
        context['soma_total'] = total_soma_acao + total_soma_fii
        
        return context