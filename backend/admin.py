from django.contrib import admin
from .models import (
    Profile,
    Course,
    Group,
    SurveyAnswers,
    Survey
)

# Register your models here.
# admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Group)
admin.site.register(SurveyAnswers)
admin.site.register(Survey)
