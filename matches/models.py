from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Player(models.Model):
    """
    Модель игрока (для полноты, хотя в матчах участвуют команды).
    """
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    team = models.CharField(max_length=100, verbose_name="Команда", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"


class SportTournament(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"


class Match(models.Model):
    location = models.CharField(max_length=200, verbose_name="Локация")
    start_time = models.DateTimeField(verbose_name="Время начала", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="Время конца", null=True, blank=True)
    team1 = models.CharField(max_length=100, verbose_name="Команда 1")
    team2 = models.CharField(max_length=100, verbose_name="Команда 2")
    score1 = models.PositiveSmallIntegerField(default=0, verbose_name="Счёт команды 1")
    score2 = models.PositiveSmallIntegerField(default=0, verbose_name="Счёт команды 2")
    winner = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Победитель",
        help_text="Оставьте пустым для несостоявшихся матчей"
    )
    
    tournament = models.ForeignKey(
        SportTournament,
        on_delete=models.SET_NULL,   
        null=True,
        blank=True,
        verbose_name="Турнир"
    )

    def __str__(self):
        return f"{self.team1} vs {self.team2} at {self.location}"

    class Meta:
        verbose_name = "Матч"
        verbose_name_plural = "Матчи"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар',
    )

    def __str__(self):
        return f'Профиль {self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


# Автоматически создаём/обновляем профиль при сохранении User
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # На случай, если профиль почему-то отсутствует
        Profile.objects.get_or_create(user=instance)