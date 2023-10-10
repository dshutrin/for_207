from django.shortcuts import render
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout

from .models import *
from .forms import *

import math
import xlsxwriter


# Create your views here.
def get_main_page(request):
	return render(request, 'main_app/start.html', {'tables': [x for x in Table.objects.all().order_by('number') if x.user]})


def get_check_list(request):
	workbook = xlsxwriter.Workbook('CheckList.xlsx')
	worksheet = workbook.add_worksheet()

	data = [
		(f'{u.surname} {u.name}', u.likes, u.dislikes) for u in Worker.objects.all()
	]

	row = 0
	for fio, l, d in (data):
		worksheet.write(row, 0, fio)
		worksheet.write(row, 1, l)
		worksheet.write(row, 2, d)
		row += 1
	workbook.close()

	with open('CheckList.xlsx', 'rb') as file:
		response = HttpResponse(file.read(), content_type='application/xlsx')
		response['Content-Disposition'] = 'attachment; filename="CheckList.xlsx"'
		return response


def get_table_vars(request, number):
	return render(request, 'main_app/choices.html', {'number': number})


def like(request, number):
	table = Table.objects.filter(number=number)
	if len(table) < 1:
		return HttpResponseRedirect('/')
	table = table[0]
	table.user.likes += 1
	table.user.save()
	return render(request, 'main_app/liked.html', {'number': table.number})


def dislike(request, number):
	table = Table.objects.filter(number=number)
	if len(table) < 1:
		return HttpResponseRedirect('/')
	table = table[0]
	table.user.dislikes += 1
	table.user.save()
	return render(request, 'main_app/disliked.html', {'number': table.number})


def adminka(request):
	def get_likes(table):
		if table.user:
			return table.user.likes
		return -1

	if request.user.is_authenticated:
		tables = Table.objects.all().order_by('number')
		tables = sorted(tables, key=get_likes, reverse=True)
		counts = [x.user.likes for x in tables if x.user] + [x.user.dislikes for x in tables if x.user]
		if counts:
			max_count = math.ceil(max(counts) * 1.2) or 0
		else:
			max_count = 0

		return render(request, 'main_app/adminka.html', {
			'tables': tables,
			'max_count': max_count
		})

	else:
		return HttpResponseRedirect('/auth')


def auth_def(request):
	if request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/adminka')
		else:
			return render(request, 'main_app/auth_page.html', {'form': LogForm()})
	elif request.method == 'GET':
		return render(request, 'main_app/auth_page.html', {'form': LogForm()})


def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')


def user_list(request):
	return render(request, 'main_app/user_list.html', {
		'tables': Table.objects.all().order_by('number'),
		'workers': Worker.objects.all()
	})


def table_detail(request, table_id):
	table = Table.objects.filter(id=table_id)

	if len(table):
		table = Table.objects.get(id=table_id)
		workers = [
			# Свободные работники
			worker for worker in Worker.objects.all() if not (worker in [t.user for t in Table.objects.all()])
		]
		return render(request, 'main_app/table_detail.html', {
			'table': table,
			'workers': workers
		})
	return HttpResponseRedirect('/adminka/user_list')


def set_new_worker(request, table_id, worker_id):
	table = Table.objects.filter(id=table_id)

	if worker_id == 0:
		table[0].clear_user()
	else:
		worker = Worker.objects.filter(id=worker_id)

		if len(table) and len(worker):
			table[0].user = worker[0]
			table[0].save()
	return HttpResponseRedirect(f'/adminka/user_list/tables/{table_id}')


def add_table(request):
	numbers = [t.number for t in Table.objects.all().order_by('number')]
	print(numbers)
	a = list(range(numbers[0], numbers[-1] + 1))
	if numbers == a:
		Table.objects.create(user=None, number=numbers[-1]+1)
	else:
		for i in range(len(numbers) - 1):
			if numbers[i + 1] - numbers[i] > 1:
				Table.objects.create(user=None, number=i+2)
				break
	return HttpResponseRedirect('/adminka/user_list')


def add_user(request):
	add_form = AddForm()
	if request.method == 'GET':
		return render(request, 'main_app/add_user_page.html', {'form': add_form})
	else:
		add_form = AddForm(request.POST)

		if add_form.is_valid():
			cd = add_form.cleaned_data

			# Тут создание пользователя по данным из формы
			worker = Worker.objects.create(
				name=cd['name'],
				surname=cd['surname'],
				likes=0,
				dislikes=0
			)
			worker.save()
			return HttpResponseRedirect('/adminka/user_list')

		return render(request, 'main_app/add_user_page.html', {'form': add_form})


def worker_detail(request, worker_id):
	worker = Worker.objects.filter(id=worker_id)

	if len(worker):
		worker = Worker.objects.get(id=worker_id)
		return render(request, 'main_app/worker_detail.html', {
			'worker': worker
		})

	return HttpResponseRedirect('/adminka/user_list')


def set_null_dislikes(request, worker_id):
	worker = Worker.objects.filter(id=worker_id)

	if len(worker):
		worker = Worker.objects.get(id=worker_id)
		worker.dislikes = 0
		worker.save()

	return HttpResponseRedirect('/adminka/user_list/workers/' + str(worker_id))


def set_null_likes(request, worker_id):
	worker = Worker.objects.filter(id=worker_id)

	if len(worker):
		worker = Worker.objects.get(id=worker_id)
		worker.likes = 0
		worker.save()

	return HttpResponseRedirect('/adminka/user_list/workers/' + str(worker_id))


def delete_worker(request, worker_id):
	worker = Worker.objects.filter(id=worker_id)

	if len(worker):
		return render(request, 'main_app/del_user.html', {'worker': worker[0]})

	return HttpResponseRedirect('/adminka/user_list')


def delete_worker_yes(request, worker_id):
	worker = Worker.objects.filter(id=worker_id)

	if len(worker):
		worker[0].delete()

	return HttpResponseRedirect('/adminka/user_list')


def delete_worker_no(request, worker_id):
	return HttpResponseRedirect(f'/adminka/user_list/workers/{worker_id}')
