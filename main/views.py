from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .service import LargeResultsSetPagination
from account.permissions import IsActivePermission
from .permissions import IsAuthorPermission
from .serializers import *
from .models import *

class PermissionMixin:
    def get_permissions(self):
        if self.action == "create":
            permissions = [IsActivePermission]
        elif self.action in ["update", "partial_update", "destroy"]:
            permissions = [IsAuthorPermission]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]

class CategoryListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SurveyViewSet(PermissionMixin, viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'author__email']
    filterset_fields = ['category']
    ordering_fields = '__all__'

class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class SumbitionViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Sumbition.objects.all()
    serializer_class = SumbitionSerializer

class ReviewCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

class AddRatingViewSet(PermissionMixin,viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = CreateRatingSerializer

class InfoUserViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = InfoUser.objects.all()
    serializer_class = InfoUserSerializer

class LikeView(PermissionMixin, viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    # @action(detail=False, methods=["GET", ])
    # def favorite(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(author=request.user)
    #     serializer = LikeSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data, status=200)
