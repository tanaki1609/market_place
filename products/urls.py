from django.urls import path
from . import views
from .constants import LIST_CREATE, ITEM

urlpatterns = [
    path('test/', views.test_api_view),
    path('', views.ProductListCreateAPIView.as_view()),  # GET->list, POST->create
    path('<int:id>/', views.product_detail_api_view),  # GET->item, PUT->update, DELETE->destroy
    path('tags/', views.TagListCreateAPIView.as_view()),  # GET -> list, POST -> create
    path('tags/<int:id>/', views.TagDetailAPIView.as_view()),
    path('categories/', views.CategoryModelViewSet.as_view(LIST_CREATE)),  # GET -> list, POST -> create
    path('categories/<int:id>/', views.CategoryModelViewSet.as_view(ITEM))
]
