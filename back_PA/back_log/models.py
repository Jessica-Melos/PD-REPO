from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone




class Area(models.Model):
    id_area = models.AutoField(primary_key=True)
    name_area = models.CharField(max_length=80, unique=True)
    id_diretoria = models.ForeignKey('Diretoria', on_delete=models.DO_NOTHING, db_column='id_diretoria')


    class Meta:
        db_table = 'area'
        unique_together = (('id_area', 'id_diretoria'),)


class Diretoria(models.Model):
    id_diretoria = models.AutoField(primary_key=True)
    name_diretoria = models.CharField(max_length=45, unique=True)


    class Meta:
        db_table = 'diretoria'


class Gestor(models.Model):
    id_gestor = models.AutoField(primary_key=True, db_column='id_gestor')
    name_gestor = models.CharField(max_length=45)
    email_gest = models.EmailField(max_length=45)
    id_diretoria = models.ForeignKey('Diretoria', on_delete=models.DO_NOTHING, db_column='id_diretoria')
    identificador = models.CharField(max_length=4, blank=True, null=True)
    changed_password = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        db_table = 'gestor'
        unique_together = (('id_gestor', 'id_diretoria'),)



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

        from django.db import models

class PA(models.Model):
    id_pa = models.AutoField(primary_key=True)
    id_gestor = models.ForeignKey('Gestor', on_delete=models.CASCADE)
    nome = models.CharField(max_length=405, null=False, blank=True) # nome
    mnemonico = models.CharField(max_length=405, null=False, blank=True)

    class Meta:
        db_table = 'back_log_pa'
    def __str__(self):
        return self.mnemonico

class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    duracao_horas = models.PositiveIntegerField() # carga horária
    id_pa = models.ForeignKey('PA', on_delete=models.CASCADE, db_column='id_pa', null=True) # pk do pa

    def __str__(self):
        return self.nome
        
class Colaborador(models.Model):
    id_colaborador = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=275)
    id_gestor = models.ForeignKey('Gestor', on_delete=models.CASCADE, null=True, blank=True) # deletar ssa

    id_pa = models.ForeignKey('PA', on_delete=models.CASCADE, db_column='id_pa', null=True)  # Relacionamento restaurado

    def __str__(self):
        return self.nome 