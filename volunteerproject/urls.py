from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from volunteerapi.views import CauseAreaView, register_user, login_user, VolunteerUsersView, JobPostsView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'causeareas', CauseAreaView, 'causeareas')
router.register(r'volunteers', VolunteerUsersView, 'volunteers')
router.register(r'posts', JobPostsView, 'posts')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
