from django.urls import path
from .views import user_register, user_login, dash_board, logout_view, edit_profile, user_order_history
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', user_register),
    path('login/', user_login),
    path('dashboard/', dash_board),
    path('logout/', logout_view),
    path('update/<str:pk>/', edit_profile, name="update_profile"),
    path('user-history/', user_order_history),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),
]