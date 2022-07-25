from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('entrar/', views.login_user, name='entrar'),
    path('sair/', views.logout_user, name='sair'),
    path('registrar/', views.register_user, name='registrar'),

    # Recuperar senha
    path('recuperar-senha/',
         auth_views.PasswordResetView.as_view(
             template_name='auth/recuperar-senha.html',
             title=' - Recuperar senha',
             success_url=reverse_lazy("usuarios:password_reset_done"),
             email_template_name='auth/recuperar-senha-email.html'
         ), name='password_reset'),
    path('recuperar-senha/enviado/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='auth/recuperar-senha-solicitada.html',
             title=' - Recuperar senha - Email enviado'
         ), name='password_reset_done'),
    path('recuperar-senha-confirmar/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='auth/recuperar-senha-confirmar.html',
             success_url=reverse_lazy("usuarios:password_reset_complete")
         ), name='password_reset_confirm'),
    path('recuperar-senha-sucesso/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='auth/recuperar-senha-sucesso.html'
         ), name='password_reset_complete'),

    # Alterar senha
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(
        success_url = reverse_lazy('usuarios:senha_alterada_sucesso'),
        template_name='auth/alterar-senha.html',
        title=' - Alterar senha'
    ), name='alterar_senha'),
    path('alterar-senha/sucesso/', auth_views.PasswordChangeDoneView.as_view(
        template_name='auth/alterar-senha-sucesso.html'
    ), name='senha_alterada_sucesso'),
]
