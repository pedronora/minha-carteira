from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Acao, AcaoByUser, Operacao
from .forms import AddAcaoForm, UpSertAcaoForm, UpSertOperacaoForm
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def upsert_operacao(form):
    tipo = form.cleaned_data['tipo']
    preco = form.cleaned_data['preco']
    qtde = form.cleaned_data['quantidade']
    custos = form.cleaned_data['custos']

    if tipo == 'V' and qtde > 0:
        qtde *= -1

    if tipo in 'CBD' and qtde < 0:
        qtde = abs(qtde)

    form.instance.quantidade = qtde
    form.instance.total_nota = preco * qtde + custos
    form.instance.contabil = form.instance.soma_quantidade = form.instance.soma_total = form.instance.preco_medio = 0


def consolidar_bd(queryset):
    operacoes = []
    for n, op in enumerate(queryset):
        if n == 0 and op.tipo != 'V':
            op.contabil = op.total_nota
            op.soma_total = op.total_nota
            op.soma_quantidade = op.quantidade
            op.preco_medio = op.total_nota / op.quantidade
            op.save(update_fields=['contabil', 'soma_total',
                    'soma_quantidade', 'preco_medio'])
        else:
            if op.tipo in 'CBD':
                ultima_operacao = queryset[n-1]
                soma_total = ultima_operacao.soma_total + op.total_nota
                soma_quantidade = ultima_operacao.soma_quantidade + op.quantidade
                op.contabil = op.total_nota
                op.soma_total = soma_total
                op.soma_quantidade = soma_quantidade
                op.preco_medio = soma_total / soma_quantidade if soma_quantidade > 0 else 0
            else:
                if n != 0:
                    ultima_operacao = queryset[n-1]
                    contabil = ultima_operacao.preco_medio * op.quantidade
                    soma_total = contabil + ultima_operacao.soma_total
                    soma_quantidade = ultima_operacao.soma_quantidade + op.quantidade

                    op.contabil = contabil
                    op.soma_quantidade = soma_quantidade
                    op.soma_total = soma_total if soma_quantidade > 0 else 0

                    op.preco_medio = soma_total / soma_quantidade if soma_quantidade > 0 else 0

            operacoes.append(op)

    Operacao.objects.bulk_update(
        operacoes, ['contabil', 'soma_total', 'soma_quantidade', 'preco_medio'])


# Create your views here.


# CRUD - Admin - Acão
class ListarAcao(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'usuarios:entrar'
    model = Acao
    template_name = 'acao/admin/listar.html'

    def test_func(self):
        return self.request.user.is_superuser


class AdicionarAcao(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = 'usuarios:entrar'
    model = Acao
    form_class = UpSertAcaoForm
    success_url = reverse_lazy('acao:listar_acao')
    template_name = 'acao/admin/adicionar.html'

    def test_func(self):
        return self.request.user.is_superuser


class DetalhesAcao(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = 'usuarios:entrar'
    model = Acao
    template_name = 'acao/admin/detalhes.html'

    def test_func(self):
        return self.request.user.is_superuser


class EditarAcao(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = 'usuarios:entrar'
    model = Acao
    form_class = UpSertAcaoForm
    success_url = reverse_lazy('acao:listar_acao')
    template_name = 'acao/admin/editar.html'

    def test_func(self):
        return self.request.user.is_superuser


class DeletarAcao(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = 'usuarios:entrar'
    model = Acao
    success_url = reverse_lazy('acao:listar_acao')
    template_name = 'acao/admin/deletar.html'

    def test_func(self):
        return self.request.user.is_superuser


# CRUD - AçãoByUser
class ListarOperacao(LoginRequiredMixin, CreateView):
    login_url = 'usuarios:entrar'
    model = AcaoByUser
    template_name = 'acao/operacao/listar.html'
    success_url = reverse_lazy('acao:listar_minhas_acoes')
    form_class = AddAcaoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        acoes_user = AcaoByUser.objects.filter(user=user)

        context['lista'] = []
        context['total'] = 0
        context['count'] = acoes_user.count()
        context['title'] = '- Ações'

        for item in acoes_user:
            filterargs = {'user': user, 'acao': item.acao}
            ultima = Operacao.objects.filter(**filterargs).last()
            if ultima:
                ultima.pk = item.pk
                context['lista'].append(ultima)
                context['total'] += ultima.soma_total
            else:
                context['lista'].append(Operacao(
                    pk=item.pk, data='0000-00-00', nr_nota=0, tipo='C', preco=0, quantidade=0, custos=0, acao=item.acao, user=user, contabil=0, total_nota=0, soma_quantidade=0, soma_total=0, preco_medio=0))

        return context

    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            messages.error(
                self.request, f'{form.cleaned_data["acao"]} já está adicionada!')
            return HttpResponseRedirect(reverse_lazy('acao:listar_minhas_acoes'))


class DeletarAcaoByUser(LoginRequiredMixin, DeleteView):
    login_url = 'usuarios:entrar'
    model = AcaoByUser
    template_name = 'acao/acaobyuser/deletar.html'
    success_url = reverse_lazy('acao:listar_minhas_acoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f' - Deletar: {self.object.acao}'
        return context

    def form_valid(self, form):
        acao_by_user = self.object
        filterargs = {'acao': acao_by_user.acao, 'user': self.request.user}
        Operacao.objects.filter(**filterargs).delete()
        acao_by_user.delete()

        messages.warning(self.request, f'{acao_by_user} deletada com sucesso!')
        
        return HttpResponseRedirect(self.get_success_url())
    


# CRUD - Operações
class CriarOperacao(LoginRequiredMixin, CreateView):
    login_url = 'usuarios:entrar'
    model = Operacao
    template_name = 'acao/operacao/adicionar_operacao.html'
    form_class = UpSertOperacaoForm

    def get_success_url(self):
        return reverse_lazy('acao:detalhes_operacoes_acao', kwargs={'pk': self.object.acao.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['acao'] = get_object_or_404(Acao, pk=self.kwargs['pk'])
        context['title'] = '- Adicionar ação'
        return context

    def form_valid(self, form):
        # Insere formulário com campos vazios
        user = self.request.user
        acao = get_object_or_404(Acao, pk=self.kwargs['pk'])
        form.instance.acao = acao
        form.instance.user = user

        upsert_operacao(form)

        super().form_valid(form)

        # Consolida demais informações do banco de dados
        filterargs = {'acao': acao, 'user': self.request.user}
        lista_operacoes = Operacao.objects.filter(**filterargs)

        consolidar_bd(lista_operacoes)
        messages.success(self.request, 'Operação adicionada com sucesso!')

        return HttpResponseRedirect(self.get_success_url())


class DetalhesOperacoesAcao(LoginRequiredMixin, ListView):
    login_url = 'usuarios:entrar'
    template_name = 'acao/operacao/detalhes_operacoes_acao.html'

    def get_queryset(self):
        self.acao = get_object_or_404(Acao, pk=self.kwargs['pk'])
        filterargs = {'acao': self.acao, 'user': self.request.user}
        return Operacao.objects.filter(**filterargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['acao'] = self.acao
        context['title'] = f'- Detalhes: {self.acao}'
        return context


class EditarOperacao(LoginRequiredMixin, UpdateView):
    login_url = 'usuarios:entrar'
    model = Operacao
    form_class = UpSertOperacaoForm
    template_name = 'acao/operacao/editar.html'

    def get_success_url(self):
        return reverse_lazy('acao:detalhes_operacoes_acao', kwargs={'pk': self.object.acao.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'- Editar: {self.object.acao}'
        return context

    def form_valid(self, form):

        upsert_operacao(form)
        super().form_valid(form)

        filterargs = {'acao': self.object.acao, 'user': self.request.user}
        lista_operacoes = Operacao.objects.filter(**filterargs)
        consolidar_bd(lista_operacoes)

        messages.success(self.request, 'Operação editada com sucesso!')

        return HttpResponseRedirect(self.get_success_url())


class DeletarOperacao(LoginRequiredMixin, DeleteView):
    login_url = 'usuarios:entrar'
    model = Operacao
    template_name = 'acao/operacao/deletar.html'

    def get_success_url(self):
        return reverse_lazy('acao:detalhes_operacoes_acao', kwargs={'pk': self.object.acao.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'- Deletar: {self.object.acao}'
        return context

    def form_valid(self, form):
        operacao_atual = self.object
        filterargs = {'acao': operacao_atual.acao, 'user': self.request.user}
        lista_filtrada = Operacao.objects.filter(**filterargs)

        operacao_atual.delete()

        consolidar_bd(lista_filtrada)

        messages.success(self.request, 'Operação deletada com sucesso!')

        return HttpResponseRedirect(self.get_success_url())
