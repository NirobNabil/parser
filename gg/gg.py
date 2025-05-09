from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('home/', views.home, name='home'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    re_path(r'^article/(?P<slug>[\w-]+)/$', views.article_detail),
    path('blog/', include('blog.urls')),
    path('class-view/', MyView.as_view(), name='class_view'),
    path('api/', my_api_view),
    url(r'^old-way/$', views.old_view),
]



from rest_framework.routers import DefaultRouter
from .views import MyViewSet

router = DefaultRouter()
router.register(r'my-resource', MyViewSet, basename='myresource')

urlpatterns = router.urls

from rest_framework_nested.routers import NestedSimpleRouter

router = SimpleRouter()
router.register(r'users', UserViewSet)
user_router = NestedSimpleRouter(router, r'users', lookup='user')
user_router.register(r'profiles', ProfileViewSet, basename='user-profiles')


response = client.get('/some/route/')