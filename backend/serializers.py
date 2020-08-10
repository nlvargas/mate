from .models import (
    Profile,
    Course,
    Group,
    SurveyAnswers,
    Survey
)
from rest_framework import serializers
from django.contrib.auth.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    # We initiate the user profile so we can get the "is_teacer" and "student_number" attributes
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('is_teacher', 'student_number', 'active')


class UserSerializer(serializers.ModelSerializer):
    # We initiate the user profile so we can get the "is_teacer" and "student_number" attributes
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile')


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'tag', 'teacher_fk')  # missing: question list


class CourseSerializer(serializers.ModelSerializer):
    teacher_fk = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'tag', 'teacher_fk', 'students', 'active')


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'number', 'course_fk')


class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'number', 'course_fk', 'members', 'active')


class SurveyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'course_fk', 'questions', 'preferences_opt', 'preferences_num')

class SurveySerializer(serializers.ModelSerializer):
    course_fk = CourseCreateSerializer()
    
    class Meta:
        model = Survey
        fields = ('id', 'questions', 'preferences_opt', 'preferences_num', 'course_fk')

class SurveyAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswers
        fields = ('id', 'student_fk', 'survey_fk', 'answers', 'preferences', 'active')
