from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router yaratish
router = DefaultRouter()
router.register(r'postlar', views.PostViewSet, basename='post')
router.register(r'izohlar', views.IzohViewSet, basename='izoh')
router.register(r'profillar', views.ProfilViewSet, basename='profil')



urlpatterns = [
    path('', views.bosh_sahifa, name='bosh_sahifa'),
    path('post/<int:post_id>/', views.post_batafsil, name='post_batafsil'),
    path('ommabop/', views.ommabop_postlar, name='ommabop'),
    path('biz-haqimizda/', views.biz_haqimizda, name='biz_haqimizda'),
    path('aloqa/', views.aloqa, name='aloqa'),
    path('portfolio/', views.portfolio, name='portfolio'),  # Yangi
    path('yangi/', views.post_yaratish, name='post_yaratish'),
    path('post/<int:post_id>/izoh/', views.post_izoh, name='post_izoh'),
    path('post/<int:post_id>/tahrirlash/', views.post_tahrirlash, name='post_tahrirlash'),
    path('post/<int:post_id>/ochirish/', views.post_ochirish, name='post_ochirish'),
    path('royxatdan-otish/', views.royxatdan_otish, name='royxatdan_otish'),
    path('profil/tahrirlash/', views.profil_tahrirlash, name='profil_tahrirlash'),
    path('profil/<str:username>/', views.profil, name='profil'),
    path('kirish/', views.kirish, name='kirish'),
    path('chiqish/', views.chiqish, name='chiqish'),
    # ... HTML viewlar

    # API Authentication
    path('api/<str:version>/kirish/', views.login_api, name='login_api'),
    path('api/<str:version>/chiqish/', views.logout_api, name='logout_api'),
    path('api/<str:version>/royxatdan-otish/', views.register_api, name='register_api'),

    # API CRUD
    path('api/<str:version>/', include(router.urls)),

]