from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from .views import  form_cad, form_log, perfil_gestor_livre, setar_banco_livre, change_password, tela_final_livre
 # EditarPAView setar_banco,
#from .views import change_password
urlpatterns = [
    path('pagina', views.form_log, name='form_log'), 
#path('perfil_gestor/', views.perfil_gestor, name='perfil_gestor'),
    path('api/token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('cadastro/', views.form_cad, name='form_cadastro'),
    path('change_password/', views.change_password, name='change_password'),
   # path('setar_banco/', setar_banco, name='setar_banco'),
   # path('tela_final/', tela_final_view, name='tela_final'),
   # path('editar_pa/', EditarPAView.as_view(), name='editar_pa'),
   path('perfil_gestor_livre/', views.perfil_gestor_livre, name='perfil_gestor_livre'),
   path('setar_banco_livre/', views.setar_banco_livre, name='setar_banco_livre'),
   path('tela-final-livre/', views.tela_final_livre, name='tela_final_livre'),
]
