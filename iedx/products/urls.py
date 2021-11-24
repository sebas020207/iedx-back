from django.urls import include, path
from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/product', views.AddProductView.as_view()),
    path('admin/product/<int:pk>', views.ProductView.as_view()),
    path('admin/products', views.AllProductsView.as_view()),
    path('admin/products/count', views.ProductCountView.as_view()),
    path('admin/product/images/<int:pk>', views.ProductImages.as_view()),
    path('admin/categories', views.CategoryView.as_view()),
    path('admin/subcategory/<int:pk>', views.SubcategoryView.as_view()),
    path('admin/supplier', views.AddSupplierView.as_view()),
    path('admin/supplier/<int:pk>', views.SupplierView.as_view()),
    path('admin/suppliers', views.AllSuppliersView.as_view()),
    path('subcategory/<int:pk>', views.PublicSubcategoryView.as_view()),
    path('products', views.PublicProductView.as_view()),
    path('subcategories', views.PublicSubcategoriesView.as_view()),
    path('suppliers', views.PublicSupplierView.as_view()),
]
