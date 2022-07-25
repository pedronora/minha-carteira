from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Acao(models.Model):
    nome = models.CharField(max_length=120)
    codigo = models.CharField(max_length=6)
    image_url = models.URLField()

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Ação'
        verbose_name_plural = 'Ações'

    def __str__(self):
        return self.codigo


class AcaoByUser(models.Model):
    acao = models.ForeignKey(Acao, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['acao']
        unique_together = ('acao', 'user')
        verbose_name = "Ação"
        verbose_name_plural = "Ações"

    def __str__(self):
        return self.acao.codigo


class Operacao(models.Model):
    TIPO_CHOICES = [
        ('C', 'Compra'),
        ('V', 'Venda'),
        ('D', 'Desdobramento'),
        ('B', 'Bonificação')
    ]

    data = models.DateField()
    nr_nota = models.IntegerField()
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    preco = models.FloatField()
    quantidade = models.IntegerField()
    custos = models.FloatField()
    acao = models.ForeignKey(Acao, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, related_name='user_acao_operacao', on_delete=models.CASCADE)
    contabil = models.FloatField()
    total_nota = models.FloatField()
    soma_quantidade = models.FloatField()
    soma_total = models.FloatField()
    preco_medio = models.FloatField()

    class Meta:
        ordering = ['data']
        verbose_name = "Operação"
        verbose_name_plural = "Operações"

    def __str__(self):
        return f'{self.data} | {self.acao} | Qtd: {self.quantidade} | Preço: R$ {self.preco:.2f}'
