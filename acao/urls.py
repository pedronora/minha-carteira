from django.urls import path
from . import views

app_name = 'acao'

urlpatterns = [
    # CRUD - Admin - Acão
    path('admin/', views.ListarAcao.as_view(), name='listar_acao'),
    path('admin/adicionar/',
         views.AdicionarAcao.as_view(), name='adicionar_acao'),
    path('admin/detalhes/<int:pk>/',
         views.DetalhesAcao.as_view(), name='detalhes_acao'),
    path('admin/editar/<int:pk>/',
         views.EditarAcao.as_view(), name='editar_acao'),
    path('admin/deletar/<int:pk>/',
         views.DeletarAcao.as_view(), name='deletar_acao'),

    # CRUD - Operações
    path('', views.ListarOperacao.as_view(), name='listar_minhas_acoes'),
    path('operacao/adicionar/<int:pk>/',
         views.CriarOperacao.as_view(), name='adicionar_operacao'),
    path('detalhes/<int:pk>/',
         views.DetalhesOperacoesAcao.as_view(), name='detalhes_operacoes_acao'),
    path('operacao/editar/<int:pk>/',
         views.EditarOperacao.as_view(), name='editar_operacao'),
    path('operacao/deletar/<int:pk>/',
         views.DeletarOperacao.as_view(), name='deletar_operacao'),

     # CRUD - AcoesByUser
     path('deletar/<int:pk>', views.DeletarAcaoByUser.as_view(), name='deletar_acao_user')
]
