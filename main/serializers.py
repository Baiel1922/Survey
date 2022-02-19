from rest_framework import serializers
from .models import Category, Survey, Question, Choice, Sumbition

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'name']

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['question', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['survey', 'text']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["choices"] = ChoiceSerializer(instance.choices.all(), many=True,
                                                         context=self.context).data
        return representation

class SumbitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sumbition
        fields = ['survey', 'answer', 'participant_email']

class SurveySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%y %H:%M:%S', read_only=True)
    class Meta:
        model = Survey
        fields = ['title', 'created_at', 'updated_at', 'author', 'category', 'image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["questions"] = QuestionSerializer(instance.questions.all(), many=True,
                                                         context=self.context).data
        return representation

