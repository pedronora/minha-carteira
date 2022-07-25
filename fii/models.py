from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class FII(models.Model):
    nome = models.CharField(max_length=120)
    codigo = models.CharField(max_length=6)
    image_url = models.URLField()

    class Meta:
        ordering = ['codigo']
        verbose_name = 'FII'
        verbose_name_plural = 'FIIs'

    def __str__(self):
        return self.codigo


class FIIByUser(models.Model):
    fii = models.ForeignKey(FII, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['fii']
        unique_together = ('fii', 'user')
        verbose_name = "FII"
        verbose_name_plural = "FIIs"

    def __str__(self):
        return self.fii.codigo


class Operacao(models.Model):
    TIPO_CHOICES = [
        ('C', 'Compra'),
        ('V', 'Venda'),
        ('D', 'Desdobramento'),
        ('A', 'Amortização')
    ]

    data = models.DateField()
    nr_nota = models.IntegerField()
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    preco = models.FloatField()
    quantidade = models.IntegerField()
    custos = models.FloatField()
    fii = models.ForeignKey(FII, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, related_name='user_fii_operacao', on_delete=models.CASCADE)
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
        return f'{self.data} | {self.fii} | Qtd: {self.quantidade} | Preço: R$ {self.preco:.2f}'
