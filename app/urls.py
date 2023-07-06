from django.urls import path
from . import views







urlpatterns = [
    path('reg', views.Register.as_view()),
    path('login',views.LoginView.as_view()),
    path('marks', views.get_data),
    path('marks/<int:hall_ticket>/',views.MarksDetailView.as_view()),
    path('get/<str:gender>/',views.GenderMarksAPIView.as_view()),
    path('highest',views.HighestMarksView.as_view()),
    path('rank',views.RankAPI.as_view()),

]
