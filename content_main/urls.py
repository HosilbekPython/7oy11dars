from tkinter.font import names

from django.urls import path


from .views import (HomePageCategoryAndProduct , CategoryFilterView , ProductDetaliViews , CommentSaveViews , DeleteCommentView
                    , ShopingView)

urlpatterns = [
    path('' , HomePageCategoryAndProduct.as_view()) ,
    path('category/<str:slug>/' , CategoryFilterView.as_view() , name = 'category_filter') ,
    path('produkt_detail/<int:product_id>/' , ProductDetaliViews.as_view() , name = 'product_detail') ,
    path('produkt_detail/<int:product_id>/comment/', CommentSaveViews.as_view(), name="save_comment"),
    path('produkt_detail_delete/<int:product_id>/comment_delete/<int:comment_id>/', DeleteCommentView.as_view(), name="delete_comment"),
    path('shoping/', ShopingView.as_view(), name="shoping"),
    path('shoping/<slug:category_slug>/', ShopingView.as_view(), name='shoping_filter'),
]