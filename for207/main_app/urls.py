from django.urls import path
from .views import *

urlpatterns = [
	path('', get_main_page),
	path('tables/<int:number>', get_table_vars),
	path('tables/<int:number>/like', like),
	path('tables/<int:number>/dislike', dislike),


	path('adminka', adminka),
	path('adminka/user_list', user_list),
	path('adminka/user_list/tables/<int:table_id>', table_detail),
	path('adminka/user_list/tables/add', add_table),
	path('adminka/user_list/tables/<int:table_id>/set_worker/<int:worker_id>', set_new_worker),
	path('adminka/user_list/workers/<int:worker_id>', worker_detail),
	path('adminka/user_list/workers/add', add_user),
	path('adminka/user_list/workers/<int:worker_id>/dislikes/set_null', set_null_dislikes),
	path('adminka/user_list/workers/<int:worker_id>/likes/set_null', set_null_likes),
	path('adminka/user_list/workers/<int:worker_id>/del', delete_worker),
	path('adminka/user_list/workers/<int:worker_id>/del/no', delete_worker_no),
	path('adminka/user_list/workers/<int:worker_id>/del/yes', delete_worker_yes),


	path('auth', auth_def),
	path('logout', logout_view)
]

