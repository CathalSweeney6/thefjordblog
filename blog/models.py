from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse

STATUS = ((0, "Draft"), (1, "Published"))

ARTICLE_CATEGORIES = (
    ('# Norway', '# Norway'),
    ('# Sweden', '# Sweden'),
    ('# Denmark', '# Denmark'),
    ('# Finland', '# Finland'),
    ('# Iceland', '# Iceland'),
    ('# Nordic', '# Nordic'),)


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="article_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    categories = models.CharField(
        max_length=50, choices=ARTICLE_CATEGORIES, default='# Nordic')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='article_like', blank=True)
    category =  models.TextField(blank=True, default='# Nordic')

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

    def get_absolute_url(self):
        """Sets absolute URL"""
        return reverse('article_detail', args=[self.article.slug])
