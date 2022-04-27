from rest_framework import serializers
from .models import *
from rest_framework.fields import ReadOnlyField

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
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ['email', 'name', 'text', 'children', 'survey']

class CreateRatingSerializer(serializers.ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = ('survey', 'star', 'author')

    def create(self, validated_data):
        request = self.context.get('request')
        # rating = Rating.objects.update_or_create(
        #     author=request.user,
        #     survey=validated_data.get('survey'),
        #     star=validated_data.get('star')
        # )
        rating, _ = Rating.objects.update_or_create(
            author=request.user,
            survey=validated_data.get('survey', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating


class LikeSerializer(serializers.ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        survey = validated_data.get('survey')

        if Like.objects.filter(author=user, survey=survey):
            return Like.objects.get(author=user, survey=survey)
        else:
            return Like.objects.create(author=user, survey=survey)


class SurveySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%y %H:%M:%S', read_only=True)
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Survey
        fields = ['id', 'title', 'created_at', 'updated_at', 'category', 'image', 'author', 'description', ]

    def create(self, validated_data):
        request = self.context.get('request')
        survey = Survey.objects.create(
            author=request.user,
            title=validated_data.get('title'),
            category=validated_data.get('category'),
            description=validated_data.get('description'),
            image=validated_data.get('image')
        )
        return survey

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["questions"] = QuestionSerializer(instance.questions.all(), many=True,
                                                         context=self.context).data
        representation["reviews"] = ReviewSerializer(instance.reviews.all(), many=True,
                                                     context=self.context).data
        representation["ratings"] = CreateRatingSerializer(instance.ratings.all(), many=True,
                                                     context=self.context).data
        representation["likes"] = Like.objects.filter(survey=instance).count()
        representation["sumbitions"] = SumbitionSerializer(instance.sumbitions.all(), many=True,
                                                           context=self.context).data
        return representation


class InfoUserSerializer(serializers.ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = InfoUser
        fields = ['id', 'author', 'name', 'surname', 'image']

    def create(self, validated_data):
        request = self.context.get('request')
        info, _ = InfoUser.objects.update_or_create(
            author=request.user,
            defaults={'name': validated_data.get('name'),
                      'surname': validated_data.get('surname'),
                      'image': validated_data.get('image')}
        )
        return info