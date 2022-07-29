
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from acao.models import AcaoByUser, Operacao as Op_Acao
from fii.models import FIIByUser, Operacao as Op_Fii

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    login_url = 'usuarios:entrar'
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' - Início'
        user = self.request.user
        acoes = AcaoByUser.objects.filter(user=user)
        fiis = FIIByUser.objects.filter(user=user)
        context['acao_count'] = acoes.count()
        context['fii_count'] = fiis.count()

        operacoes_fii = Op_Fii.objects.filter(user=user)
        operacoes_acao = Op_Acao.objects.filter(user=user)
        context['op_count'] = operacoes_fii.count() + operacoes_acao.count()

        total_soma_acao = 0
        for acao in acoes:
            ultima = operacoes_acao.filter(acao=acao.acao).last()
            if ultima:
                total_soma_acao += ultima.soma_total

        total_soma_fii = 0
        for fii in fiis:
            ultima = operacoes_fii.filter(fii=fii.fii).last()
            if ultima:
                total_soma_acao += ultima.soma_total

        context['soma_total'] = total_soma_acao + total_soma_fii
        
        return context