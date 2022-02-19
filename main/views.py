from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *
# Create your views here.

class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SurveyViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class SumbitionView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Sumbition.objects.all()
    serializer_class = SumbitionSerializer