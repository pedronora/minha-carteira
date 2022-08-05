from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import AddFIIForm, UpSertFiiForm, UpSertOperacaoForm
from .models import FII, FIIByUser, Operacao


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
            if op.tipo in 'CDS':
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
class CalcNota(LoginRequiredMixin, TemplateView):
    login_url = 'usuarios:entrar'
    template_name = 'calc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' - Divisão da Nota de Negociação'
        return context


# CRUD - Admin - FII
class ListarFII(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'usuarios:entrar'
    model = FII
    template_name = 'fii/admin/listar.html'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser


class AdicionarFII(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = 'usuarios:entrar'
    model = FII
    form_class = UpSertFiiForm
    success_url = reverse_lazy('fii:listar_fii')
    template_name = 'fii/admin/adicionar.html'

    def test_func(self):
        return self.request.user.is_superuser


class DetalhesFII(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = 'usuarios:entrar'
    model = FII
    template_name = 'fii/admin/detalhes.html'

    def test_func(self):
        return self.request.user.is_superuser


class EditarFII(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = 'usuarios:entrar'
    model = FII
    form_class = UpSertFiiForm
    success_url = reverse_lazy('fii:listar_fii')
    template_name = 'fii/admin/editar.html'

    def test_func(self):
        return self.request.user.is_superuser


class DeletarFII(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = 'usuarios:entrar'
    model = FII
    success_url = reverse_lazy('fii:listar_fii')
    template_name = 'fii/admin/deletar.html'

    def test_func(self):
        return self.request.user.is_superuser


# FII by User
class ListarOperacao(LoginRequiredMixin, CreateView):
    login_url = 'usuarios:entrar'
    model = FIIByUser
    template_name = 'fii/operacao/listar.html'
    success_url = reverse_lazy('fii:listar_meus_fiis')
    form_class = AddFIIForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        fiis_user = FIIByUser.objects.filter(user=user)

        context['lista'] = []
        context['total'] = 0
        context['count'] = fiis_user.count()
        context['title'] = '- FIIs'

        for item in fiis_user:
            filterargs = {'user': user, 'fii': item.fii}
            ultima = Operacao.objects.filter(**filterargs).last()
            if ultima:
                ultima.pk = item.pk
                context['lista'].append(ultima)
                context['total'] += ultima.soma_total
            else:
                context['lista'].append(Operacao(
                    pk=item.pk, data='0000-00-00', nr_nota=0, tipo='C', preco=0, quantidade=0, custos=0, fii=item.fii, user=user, contabil=0, total_nota=0, soma_quantidade=0, soma_total=0, preco_medio=0))

        return context

    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            messages.error(
                self.request, f'{form.cleaned_data["fii"]} já está adicionado!')
            return HttpResponseRedirect(reverse_lazy('fii:listar_meus_fiis'))


class DeletarFIIByUser(LoginRequiredMixin, DeleteView):
    login_url = 'usuarios:entrar'
    model = FIIByUser
    template_name = 'fii/fiibyuser/deletar.html'
    success_url = reverse_lazy('fii:listar_meus_fiis')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f' - Deletar: {self.object.fii}'
        return context

    def form_valid(self, form):
        fii_by_user = self.object
        filterargs = {'fii': fii_by_user.fii, 'user': self.request.user}
        Operacao.objects.filter(**filterargs).delete()
        fii_by_user.delete()

        return HttpResponseRedirect(self.get_success_url())


# CRUD - Operações
class CriarOperacao(LoginRequiredMixin, CreateView):
    login_url = 'usuarios:entrar'
    model = Operacao
    template_name = 'fii/operacao/adicionar_operacao.html'
    form_class = UpSertOperacaoForm

    def get_success_url(self):
        return reverse_lazy('fii:detalhes_operacoes_fii', kwargs={'pk': self.object.fii.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fii'] = get_object_or_404(FII, pk=self.kwargs['pk'])
        context['title'] = '- Adicionar ação'
        return context

    def form_valid(self, form):
        # Insere formulário com campos vazios
        user = self.request.user
        fii = get_object_or_404(FII, pk=self.kwargs['pk'])
        form.instance.fii = fii
        form.instance.user = user

        upsert_operacao(form)

        super().form_valid(form)

        # Consolida demais informações do banco de dados
        filterargs = {'fii': fii, 'user': self.request.user}
        lista_operacoes = Operacao.objects.filter(**filterargs)

        print(lista_operacoes.count())

        consolidar_bd(lista_operacoes)

        return HttpResponseRedirect(self.get_success_url())


class DetalhesOperacoesFII(LoginRequiredMixin, ListView):
    login_url = 'usuarios:entrar'
    template_name = 'fii/operacao/detalhes_operacoes_fii.html'
    paginate_by = 10

    def get_queryset(self):
        self.fii = get_object_or_404(FII, pk=self.kwargs['pk'])
        filterargs = {'fii': self.fii, 'user': self.request.user}
        return Operacao.objects.filter(**filterargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fii'] = self.fii
        context['title'] = f'- Detalhes: {self.fii}'
        return context


class EditarOperacao(LoginRequiredMixin, UpdateView):
    login_url = 'usuarios:entrar'
    model = Operacao
    form_class = UpSertOperacaoForm
    template_name = 'fii/operacao/editar.html'

    def get_success_url(self):
        return reverse_lazy('fii:detalhes_operacoes_fii', kwargs={'pk': self.object.fii.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'- Editar: {self.object.fii}'
        return context

    def form_valid(self, form):

        upsert_operacao(form)
        super().form_valid(form)

        filterargs = {'fii': self.object.fii, 'user': self.request.user}
        lista_operacoes = Operacao.objects.filter(**filterargs)
        consolidar_bd(lista_operacoes)

        return HttpResponseRedirect(self.get_success_url())


class DeletarOperacao(LoginRequiredMixin, DeleteView):
    login_url = 'usuarios:entrar'
    model = Operacao
    template_name = 'fii/operacao/deletar.html'

    def get_success_url(self):
        return reverse_lazy('fii:detalhes_operacoes_fii', kwargs={'pk': self.object.fii.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'- Deletar: {self.object.fii}'
        return context

    def form_valid(self, form):
        operacao_atual = self.object
        filterargs = {'fii': operacao_atual.fii, 'user': self.request.user}
        lista_filtrada = Operacao.objects.filter(**filterargs)

        operacao_atual.delete()

        consolidar_bd(lista_filtrada)

        return HttpResponseRedirect(self.get_success_url())
