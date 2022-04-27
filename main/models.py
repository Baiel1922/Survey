from django.db import models
from account.models import User
# Create your models here.
class Category(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True, verbose_name='Slug')
    name = models.CharField(max_length=50, unique=True, verbose_name='Category')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Survey(models.Model):
    title = models.CharField(max_length=255, verbose_name='Survey')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys',
                               verbose_name='Author')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='surveys',
                                 verbose_name='Category')
    image = models.ImageField(upload_to='media', blank=True, null=True, verbose_name='Image')
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions',
                               verbose_name='Survey')
    text = models.CharField(max_length=400, verbose_name='Question')
    def __str__(self):
        return f"{self.survey.title}:{self.text}"

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices',
                                 verbose_name='Question')
    text = models.CharField(max_length=255, verbose_name='Choice')

    def __str__(self):
        return f'{self.question.text}:{self.text}'

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'


class Sumbition(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='sumbitions',
                               verbose_name='Survey')
    answer = models.ManyToManyField(Choice, verbose_name='Answer')
    participant_email = models.EmailField(verbose_name='Email')
    def __str__(self):
        return self.participant_email

    class Meta:
        verbose_name = 'Sumbition'
        verbose_name_plural = 'Sumbitions'


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    survey = models.ForeignKey(Survey, verbose_name="survey", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.survey}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class RatingStar(models.Model):
    value = models.SmallIntegerField(primary_key=True, unique=True, default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating star"
        verbose_name_plural = "Rating stars"


class Rating(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='ratings')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return f'{self.survey} - {self.star}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.author} - {self.survey}'

class InfoUser(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='info_user')
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/user_image', blank=True, null=True)

    def __str__(self):
        return f'{self.name}-{self.surname}'

    class Meta:
        verbose_name = 'Info user'
        verbose_name_plural = 'Info users'
