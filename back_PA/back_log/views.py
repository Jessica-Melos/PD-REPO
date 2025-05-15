from django.contrib.auth import authenticate, login
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponseForbidden  
from .models import Gestor, Diretoria
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views import View
from back_log.models import Area
from .models import Area, Colaborador, Curso
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from .models import PA
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

def change_password(request):
    show_popup = request.session.pop('show_popup', False)  # ← aqui pega, sem mexer no banco

    if request.method == 'POST':
        email = request.POST.get('email') 
        new_password = request.POST.get('new_password') 

        try:
            gestor = Gestor.objects.get(email_gest=email) 
            
            if len(new_password) == 4 and new_password.isdigit():
                gestor.identificador = new_password  
                gestor.changed_password = True  # ← Aqui SIM você muda no banco
                gestor.save()

                messages.success(request,'Senha alterada com sucesso!')
                return redirect('form_log')
            else:
                messages.error(request, 'A senha deve conter exatamente 4 dígitos.')
        except Gestor.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
    
    return render(request, 'change_password.html', {'show_popup': show_popup})

def form_cad(request):
    diretorias = Diretoria.objects.all()
    if request.method == 'POST':

        nome = request.POST.get('name_gest')
        email = request.POST.get('email')
        identificador = request.POST.get('identificador')
        name_diretoria = request.POST.get('diretoria') 

        if not all([nome, email, identificador, name_diretoria]):
            messages.error(request, "Todos os campos são obrigatórios!")
            return render(request, 'index.html', {'diretorias': diretorias})

        if Gestor.objects.filter(email_gest=email).exists():
            messages.error(request, "Este email já está cadastrado!")
            return render(request, 'index.html', {'diretorias': diretorias})

        try:
            diretoria = Diretoria.objects.get(name_diretoria=name_diretoria)  
        except Diretoria.DoesNotExist:
            messages.error(request, "Diretoria não encontrada!")
            return render(request, 'index.html', {'diretorias': diretorias})


        gestor = Gestor.objects.create(
            name_gestor=nome,
            email_gest=email,
            identificador=identificador,
            id_diretoria=diretoria,
            changed_password=True, 
        )

        return redirect('form_log')

    return render(request, 'index.html', {'diretorias': diretorias})

def form_log(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        identificador = request.POST.get('identificador')

        gestor = authenticate(request, email=email, identificador=identificador)

        if gestor is not None:
            if not gestor.changed_password:
                login(request, gestor)
                return render(request, 'change_password.html', {'email': email, 'show_popup': True})

            login(request, gestor)
            refresh = RefreshToken.for_user(gestor)
            refresh['email_gest'] = gestor.email_gest
            access_token = str(refresh.access_token)


            pa = PA.objects.filter(id_gestor=gestor).first()
            if pa and Curso.objects.filter(id_pa=pa).exists():
                response = redirect('tela_final')
            else:
                response = redirect('perfil_gestor')

            response.set_cookie('access_token', access_token, httponly=True, secure=True)
            return response

        else:
            messages.error(request, 'E-mail ou identificador inválidos.')

    return render(request, 'index.html')
"""
def perfil_gestor(request):
    token = request.COOKIES.get('access_token')

    if not token:
        return HttpResponseForbidden('Acesso negado. Token não encontrado.')

    try:
        validated_token = JWTAuthentication().get_validated_token(token)
        user_email = validated_token.get('email_gest')

        gestor = Gestor.objects.get(email_gest=user_email)
        nome_completo = gestor.name_gestor
        primeiro_nome = nome_completo.split()[0].capitalize() 

        colaboradores = Colaborador.objects.filter(id_gestor=gestor)

        return render(request, 'perfil_gestor.html', {
            'gestor': gestor,
            'colaboradores': colaboradores,
            'nome_gestor': primeiro_nome # Adiciona ao contexto
        })

    except AuthenticationFailed:
        return HttpResponseForbidden('Acesso negado. Token inválido.')
    except Gestor.DoesNotExist:
        return HttpResponseForbidden(f'Gestor com o e-mail {user_email} não encontrado no banco de dados.')
"""
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)


        user = self.user
        data['email_gest'] = user.email_gest

        return data

def setar_banco_livre(request):
    # Simula existência de um PA (Plano de Aprendizagem)
    pa_fake = {'nome_pa': 'Plano Exemplo'}

    return render(request, 'perfil_gestor.html', {
        'pa': pa_fake
    })


def colaboradores_do_gestor(request):
    gestor_logado = Gestor.objects.get(email_gest=request.user.email) 
    colaboradores = Colaborador.objects.filter(id_gestor=gestor_logado)
    
    return render(request, 'sua_template.html', {
        'colaboradores': colaboradores
    })


"""
def editar_pa(request):
    token = request.COOKIES.get('access_token')
    if not token:
        return HttpResponseForbidden('Acesso negado. Token não encontrado.')

    try:
        validated_token = JWTAuthentication().get_validated_token(token)
        user_email = validated_token.get('email_gest')

        gestor = get_object_or_404(Gestor, email_gest=user_email)
        request.user = gestor

        pa = PA.objects.filter(id_gestor=gestor).first()
        if not pa:
            return HttpResponseForbidden('PA não encontrado para o gestor.')

        if request.method == "POST":
            nomes = request.POST.getlist('cursos[]')
            cargas = request.POST.getlist('cargas[]')

            if not nomes or not cargas or len(nomes) != len(cargas):
                return JsonResponse({'erro': 'Listas inválidas'}, status=400)

            # Conjunto de novos cursos vindos do front
            novos_cursos = set((nome.strip(), int(carga)) for nome, carga in zip(nomes, cargas))

            # Conjunto de cursos que já estão no banco
            cursos_atuais = Curso.objects.filter(id_pa=pa)
            cursos_atuais_set = set((curso.nome.strip(), curso.duracao_horas) for curso in cursos_atuais)

            # Determinar cursos a remover (que não estão na nova lista)
            cursos_para_remover = cursos_atuais.filter(~Q(nome__in=[nome for nome, _ in novos_cursos]) |
                                                       ~Q(duracao_horas__in=[horas for _, horas in novos_cursos]))

            # Remove cursos antigos que não estão mais na lista
            cursos_para_remover.delete()

            # Adiciona apenas os cursos que não existem ainda
            for nome, carga in novos_cursos - cursos_atuais_set:
                Curso.objects.create(nome=nome, duracao_horas=carga, id_pa=pa)

            return redirect('tela_final')

        cursos = Curso.objects.filter(id_pa=pa)
        colaboradores = Colaborador.objects.filter(id_gestor=gestor)
        nome_completo = gestor.name_gestor
        primeiro_nome = nome_completo.split()[0].capitalize()

        return render(request, 'edition.html', {
            'gestor': gestor,
            "pa": pa,
            "cursos": cursos,
            'colaboradores': colaboradores,
            'nome_gestor': primeiro_nome
        })

    except Exception as e:
        return HttpResponseForbidden(f'Acesso negado. Erro ao validar o token: {str(e)}')

"""

"""
def tela_final_view(request):
    token = request.COOKIES.get('access_token')

    if not token:
        return HttpResponseForbidden('Acesso negado. Token não encontrado.')

    try:
        validated_token = JWTAuthentication().get_validated_token(token)
        user_email = validated_token.get('email_gest')

        gestor = Gestor.objects.get(email_gest=user_email)

        nome_completo = gestor.name_gestor
        primeiro_nome = nome_completo.split()[0].capitalize()

        pa = PA.objects.filter(id_gestor=gestor).first()

        if not pa:
            return HttpResponseForbidden('Nenhum PA encontrado para este gestor.')

        cursos = Curso.objects.filter(id_pa=pa)

        total_horas = sum(curso.duracao_horas for curso in cursos)

        return render(request, 'tela_final.html', {
            "pa": pa,
            'gestor': gestor,
            'cursos': cursos,
            'total_horas': total_horas,
            'nome_gestor': primeiro_nome  # Adiciona ao contexto
        })

    except AuthenticationFailed:
        return HttpResponseForbidden('Acesso negado. Token inválido.')
    except Gestor.DoesNotExist:
        return HttpResponseForbidden(f'Gestor com o e-mail {user_email} não encontrado.')
    except Exception as e:
        return HttpResponseForbidden(f'Erro inesperado: {str(e)}')
        print("Cursos encontrados:", cursos.count())
"""
# TREI-AREA-2025-  mudar a função gerar mnemonico para gerar a partir da rea do gestor com a fstring.
# verificar se maida ainda é "diretoria" 
# preencher banco novamente
# mnemonico já existe, ele tem apenas que adicionar cursos da area no PA que já existe
# adicionar lista de bia no banco como nome do PA e seu gestor, mas com curso vazio
def perfil_gestor_livre(request):
    # Simula dados do gestor e colaboradores
    gestor_fake = {'name_gestor': 'Maria Oliveira'}
    nome_gestor = gestor_fake['name_gestor'].split()[0].capitalize()

    colaboradores_fake = [
        {'nome': 'João Silva'},
        {'nome': 'Ana Costa'},
        {'nome': 'Roberto Lima'}
    ]

    return render(request, 'perfil_gestor.html', {
        'gestor': gestor_fake,
        'colaboradores': colaboradores_fake,
        'nome_gestor': nome_gestor
    })

def tela_final_livre(request):
    # Simula dados do gestor
    gestor_fake = {'name_gestor': 'Carlos Pereira'}
    nome_gestor = gestor_fake['name_gestor'].split()[0].capitalize()

    # Simula um PA
    pa_fake = {'nome_pa': 'Plano Anual 2025', 'mnemonico': 'PA2025'}

    # Simula lista de cursos
    cursos_fake = [
        {'nome': 'Curso de Liderança', 'duracao_horas': 10},
        {'nome': 'Gestão de Projetos', 'duracao_horas': 12},
        {'nome': 'Comunicação Eficaz', 'duracao_horas': 8}
    ]

    total_horas = sum(curso['duracao_horas'] for curso in cursos_fake)

    return render(request, 'tela_final.html', {
        'gestor': gestor_fake,
        'pa': pa_fake,
        'cursos': cursos_fake,
        'total_horas': total_horas,
        'nome_gestor': nome_gestor
    })