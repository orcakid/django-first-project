from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name="home"),
    path("signup/", signup, name="signup"),
    path('tasks/', tasks, name='tasks'),
    path('logout/', signout, name='logout'),
    path('signin/', signin, name='signin'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>', task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', task_complete, name='task_complete'),
    path('tasks/<int:task_id>/delete', task_delete, name='task_delete'),
    path('tasks/complete_tasks', get_comp_tasks, name='complete_tasks')
]
