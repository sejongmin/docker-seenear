from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
routin_detail = RoutinViewSet.as_view({
    "get": "retrive",
    "put": "update",
    "delete": "destroy"
})

urlpatterns = [
    path("user/signup", signup),
    path("user/signup/", signup),
    path("user/login", login),
    path("user/login/", login),
    path("user/logout", logout),
    path("user/logout/", logout),

    path('family', get_family),
    path('family/', get_family),
    path('family/join', join_family),
    path('family/join/', join_family),
    path('family/member', get_members),
    path('family/member/', get_members),
    path('family/update', update_family),
    path('family/update/', update_family),

    path('routin', get_routins),
    path('routin/', get_routins),
    path('routin/create', create_routin),
    path('routin/create/', create_routin),
    path('routin/<int:pk>', routin_detail),
    path('routin/<int:pk>/', routin_detail),
]
