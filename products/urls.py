from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_api_view),
    path('', views.product_list_api_view),  # GET->list, POST->create
    path('<int:id>/', views.product_detail_api_view),  # GET->item, PUT->update, DELETE->destroy
]
