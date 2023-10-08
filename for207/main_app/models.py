from django.db import models


# Create your models here.
class Model(models.Model):
	objects = models.Manager()

	class Meta:
		abstract = True


class Worker(Model):
	name = models.CharField(max_length=100, verbose_name='Имя работника')
	surname = models.CharField(max_length=100, verbose_name='Фамилия работника')
	likes = models.IntegerField(verbose_name='Лайки', default=0)
	dislikes = models.IntegerField(verbose_name='Дизлайки', default=0)

	def __str__(self):
		return f'{self.name} {self.surname}'


class Table(Model):
	number = models.IntegerField(verbose_name='Номер стола')
	user = models.ForeignKey(Worker, verbose_name='Работник', on_delete=models.SET_NULL, null=True, default=None, blank=True)

	def clear_user(self):
		self.user = None
		self.save()

	def __str__(self):
		return f'Стол №{self.number} ({self.user})'
