from django.forms import *


class LogForm(Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control text-center'

	username = CharField(label='Имя пользователя', max_length=255)
	password = CharField(label='Пароль', widget=PasswordInput())


class AddForm(Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control text-center'

	name = CharField(label='Имя работника', max_length=255)
	surname = CharField(label='Фамилия работника', max_length=255)
