from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it is not already set
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 'PB', 'Published'
        DRAFT = 'DF', 'Draft'

    SECTION = {
        'Recent': 'Recent',
        'Popular': 'Popular',
        'Trending': 'Trending',
    }
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='blogs_author')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=Status.choices,
                              max_length=2, default=Status.DRAFT)
    section = models.CharField(
        choices=SECTION, max_length=10, default=SECTION['Recent'])
    main_post = models.BooleanField(default=False)
    views = models.PositiveBigIntegerField(default=0)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='blog_likes', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it is not already set
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.category}"

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    blog_id = models.IntegerField(null=True, blank=True)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateField(default=timezone.now)
    website = models.URLField(null=True, blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def save(self, *args, **kwargs):
        if not self.blog_id:  # Set blog_id if it is not already set
            self.blog_id = self.post.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
