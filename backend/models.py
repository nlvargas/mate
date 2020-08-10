from django.db.models import (
    Model,
    OneToOneField,
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    ManyToManyField,
    IntegerField,
    SmallIntegerField
)
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.postgres.fields import JSONField


class Profile(Model):
    user = OneToOneField(
        User,
        related_name='profile',
        on_delete=CASCADE
    )
    is_teacher = BooleanField(default=False)
    student_number = CharField(max_length=30, null=True)
    active = BooleanField(default=True)


class Course(Model):
    name = CharField(max_length=40)
    tag = CharField(max_length=20)
    teacher_fk = ForeignKey(
        User,
        on_delete=CASCADE,
    )
    students = ManyToManyField(
        User,
        related_name='students',
        blank=True
    )
    active = BooleanField(default=True)


class Group(Model):
    name = CharField(max_length=20)
    number = SmallIntegerField(default=0)
    course_fk = ForeignKey(
        Course,
        on_delete=CASCADE
    )
    members = ManyToManyField(
        User,
        related_name='members',
        blank=True
    )
    active = BooleanField(default=True)


class Survey(Model):
    course_fk = ForeignKey(
        Course,
        on_delete=CASCADE
    )
    questions = JSONField()
    """
    questions = {
        "Genero": {"options": ["M", "F"], "question": "¿Genero?"},
        "Area": {"options": ["Finanzas", "Gestion", "Estudiante"], "question": "¿Que estudiaste?"},
        "Comuna": {"options": ["RM", "No RM"], "question": "¿De donde eres?"} ,
        "Carrera": {"options": ["Ingenieria", "Medicina", "Periodismo", "Teatro"], "question": "¿Carrera?"}
    }
    """
    preferences_num = IntegerField()
    preferences_opt = JSONField()
    """
    preferences_opt = {
        "Dieta Vegana": {"min": 0, "max": 10, "description": "blabla bla"},
        "Mitigacion de huella de carbono y plantaciones forestales": {"min": 0, "max": 10, "description": ""},
        "Rol social de las Aplicaciones de Servicios de Transporte": {"min": 0, "max": 10, "description": "blabla bla"},
        "Reciclaje": {"min": 0, "max": 10, "description": "blabla bla"}
    }
    """
    active = BooleanField(default=True)


class SurveyAnswers(Model):
    student_fk = ForeignKey(
        User,
        on_delete=CASCADE
    )
    survey_fk = ForeignKey(
        Survey,
        on_delete=CASCADE
    )
    answers = JSONField()
    """
    answers = {
        "Genero": "M",
        "Area": "Finanzas",
        "Comuna": "RM",
        "Carrera": "Ingenieria"
    }
    """
    preferences = JSONField()
    """
    preferences_opt = {
        "Dieta Vegana": 1,
        "Mitigacion de huella de carbono y plantaciones forestales": 4,
        "Rol social de las Aplicaciones de Servicios de Transporte": 2,
        "Reciclaje": 3
    }
    """
    active = BooleanField(default=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
        if instance.is_superuser:
            Profile.objects.create(user=instance)
