from django.urls import path
from . import views

app_name = 'fii'

urlpatterns = [
    # CRUD - Admin - Acão
    path('admin/', views.ListarFII.as_view(), name='listar_fii'),
    path('admin/adicionar/',
         views.AdicionarFII.as_view(), name='adicionar_fii'),
    path('admin/detalhes/<int:pk>/',
         views.DetalhesFII.as_view(), name='detalhes_fii'),
    path('admin/editar/<int:pk>/',
         views.EditarFII.as_view(), name='editar_fii'),
    path('admin/deletar/<int:pk>/',
         views.DeletarFII.as_view(), name='deletar_fii'),

    # CRUD - Operações
    path('', views.ListarOperacao.as_view(), name='listar_meus_fiis'),
    path('operacao/adicionar/<int:pk>/',
         views.CriarOperacao.as_view(), name='adicionar_operacao'),
    path('detalhes/<int:pk>/',
         views.DetalhesOperacoesFII.as_view(), name='detalhes_operacoes_fii'),
    path('operacao/editar/<int:pk>/',
         views.EditarOperacao.as_view(), name='editar_operacao'),
    path('operacao/deletar/<int:pk>/',
         views.DeletarOperacao.as_view(), name='deletar_operacao'),

    # CRUD - AcoesByUser
    path('deletar/<int:pk>', views.DeletarFIIByUser.as_view(),
         name='deletar_fii_user'),

    path('divisao/', views.CalcNota.as_view(), name='divisao')
]
