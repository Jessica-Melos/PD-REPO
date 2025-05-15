from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Gestor
from rest_framework.authtoken.models import Token

class EmailBackend(BaseBackend):

    def authenticate(self, request, email=None, identificador=None, **kwargs):
        try:

            gestor = Gestor.objects.get(email_gest=email)
            print(f"Usuário encontrado: {gestor.email_gest}")


            if gestor and gestor.identificador == identificador:

                return gestor
            else:
                print("Identificador incorreto.")
                return None
        except Gestor.DoesNotExist:
            print("Usuário não encontrado.")
            return None