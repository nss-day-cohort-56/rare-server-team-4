"""app_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_api.views import register_user, login_user
from rest_framework import routers
from app_api.views import CategoryView, PostView, ProfileView, CommentView, ReactionView, TagView, SubscriptionView, DemoteView, DeactivateView
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostView, 'post')
router.register(r'categories', CategoryView, 'category')
router.register(r'profiles', ProfileView, 'profile')
router.register(r'tags', TagView, 'tag')
router.register(r'comments', CommentView, 'comment')
router.register(r'demotes', DemoteView, 'demote')
router.register(r'deactives', DeactivateView, 'deactive')

router.register(r'profileDetails', ProfileView, 'profile')

router.register(r'reactions', ReactionView, 'reaction')

router.register(r'subscriptions', SubscriptionView, 'subscription')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
