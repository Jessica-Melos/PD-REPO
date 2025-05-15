from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import JsonResponse
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)


        user = self.user
        data['email_gest'] = user.email_gest 

        return data


        from django.http import JsonResponse
from back_log.models import Diretoria, Area







#talvez eu não use essa estrutura
'''def criar_estrutura(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tipo = data.get('tipo')
        estrutura = data.get('estrutura')

        if tipo == "subarea":
            subarea_name = data.get('subarea')
            subarea_abreviada = subarea_name[:5].upper()  
            estrutura += f"/{subarea_abreviada}"


            Subarea.objects.create(
                name_subarea=subarea_name,
                id_area=data.get('id_area'),
                id_diretoria=request.user.diretoria,
            )

        return JsonResponse({'estrutura': estrutura})
'''