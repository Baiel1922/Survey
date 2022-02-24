from rest_framework import serializers
from .models import Category, Survey, Question, Choice, Sumbition, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["choices"] = ChoiceSerializer(instance.choices.all(), many=True,
                                                         context=self.context).data
        return representation

class SumbitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sumbition
        fields = "__all__"

class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class RecursiveSerializer(serializers.ModelSerializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление комментария"""
    class Meta:
        model = Review
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ['email', 'name', 'text', 'children', 'survey']

class SurveySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%y %H:%M:%S', read_only=True)
    class Meta:
        model = Survey
        fields = ['title', 'created_at', 'updated_at', 'author', 'category', 'image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["questions"] = QuestionSerializer(instance.questions.all(), many=True,
                                                         context=self.context).data
        representation["reviews"] = ReviewSerializer(instance.reviews.all(), many=True,
                                                     context=self.context).data
        return representation

