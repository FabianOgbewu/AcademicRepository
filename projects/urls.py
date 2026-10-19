from django.urls import path
from . import views

urlpatterns = [
    path('', views.public_archive, name='public_archive'),  # <-- THIS TIES UP THE EMPTY BASE PATH!
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('submit/', views.submit_project, name='submit_project'),
    path('supervisor/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('review/<int:project_id>/', views.review_project, name='review_project'),
]
