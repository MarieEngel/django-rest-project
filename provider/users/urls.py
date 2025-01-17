# Source: https://www.django-rest-framework.org/tutorial/quickstart/

from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.urlpatterns import format_suffix_patterns
from users import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)

router.register(r"posts", views.PostViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('uploads/', views.ImageView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


