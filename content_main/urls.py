from tkinter.font import names

from django.urls import path


from .views import HomePageCategoryAndProduct , CategoryFilterView

urlpatterns = [
    path('' , HomePageCategoryAndProduct.as_view()) ,
    path('category/<str:slug>/' , CategoryFilterView.as_view() , name = 'category_filter')
]