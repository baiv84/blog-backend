from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    """Post model implementation"""
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Текст")
    slug = models.SlugField("Название в виде url", max_length=200)
    image = models.ImageField("Картинка")
    published_at = models.DateTimeField("Дата и время публикации")

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        limit_choices_to={'is_staff': True})
    likes = models.ManyToManyField(
        User,
        related_name="liked_posts",
        verbose_name="Кто лайкнул",
        blank=True)

    def __str__(self):
        """Post model string representation"""
        return self.title

    def get_absolute_url(self):
        """Get absolute URL"""
        return reverse('post_detail', args={'slug': self.slug})

    class Meta:
        """Setup meta class"""
        ordering = ['-published_at']
        verbose_name = 'пост'
        verbose_name_plural = 'посты'


class Comment(models.Model):
    """Comment model implementation"""
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        verbose_name="Пост, к которому написан")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор")

    text = models.TextField("Текст комментария")
    published_at = models.DateTimeField("Дата и время публикации")

    def __str__(self):
        """Comment model string representation"""
        return f"{self.author.username} under {self.post.title}"

    class Meta:
        """Setup meta class"""
        ordering = ['published_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
