from django.urls import path
from transactions import views

urlpatterns = [
    # Transactions
    path('transactions/create/', views.TransactionCreateAPIView.as_view(), name='create-transaction'),
    path('transactions/', views.TransactionListAPIView.as_view(), name='list-transactions'),
    path('transactions/<str:pk>/details/', views.TransactionDetailAPIView.as_view(), name='details-transaction'),
    path('transactions/<str:pk>/update/', views.TransactionUpdateAPIView.as_view(), name='update-transaction'),
    path('transactions/<str:pk>/delete/', views.TransactionDeleteAPIView.as_view(), name='delete-transaction'),

    # Categories
    path('categories/create/', views.CategoryCreateAPIView.as_view(), name='create-category'),
    path('categories/', views.CategoryListAPIView.as_view(), name='list-categories'),
    path('categories/<str:pk>/update/', views.CategoryUpdateAPIView.as_view(), name='update-category'),
    path('categories/<str:pk>/delete/', views.CategoryDeleteAPIView.as_view(), name='delete-category'),

    # Customer endpoints
    path('customers/create/', views.CustomerCreateAPIView.as_view(), name='create-customer'),
    path('customers/', views.CustomerListAPIView.as_view(), name='list customer'),
    path('customers/<str:reference_id>/details/', views.CustomerDetailsAPIView.as_view(), name='details-customer'),
    path('customers/<str:reference_id>/update/', views.CustomerUpdateAPIView.as_view(), name='update-customer'),
    path('customers/<str:reference_id>/delete/', views.CustomerDeleteAPIView.as_view(), name='delete-customer'),

    # Analytics
    path('dashboard/summary/', views.DashboardSummaryAPIView.as_view(), name='dashboard-summary'),
    path('customers/due/', views.CustomerDueListAPIView.as_view(), name='customer-due-list'),
    path('reports/monthly/', views.MonthlyReportAPIView.as_view(), name='monthly-report'),
    path('ai/forecast/', views.AIForecastAPIView.as_view(), name='ai-forecast'),
    
    # Product Categories
    path('product-categories/create/', views.ProductCategoryCreateAPIView.as_view(), name='create-product-category'),
    path('product-categories/', views.ProductCategoryListAPIView.as_view(), name='list-product-categories'),
    path('product-categories/<str:pk>/details/', views.ProductCategoryDetailAPIView.as_view(), name='details-product-category'),
    path('product-categories/<str:pk>/update/', views.ProductCategoryUpdateAPIView.as_view(), name='update-product-category'),
    path('product-categories/<str:pk>/delete/', views.ProductCategoryDeleteAPIView.as_view(), name='delete-product-category'),

    # Products
    path('products/create/', views.ProductCreateAPIView.as_view(), name='create-product'),
    path('products/', views.ProductListAPIView.as_view(), name='list-products'),
    path('products/<str:pk>/details/', views.ProductRetrieveAPIView.as_view(), name='details-product'),
    path('products/<str:pk>/update/', views.ProductUpdateAPIView.as_view(), name='update-product'),
    path('products/<str:pk>/delete/', views.ProductDeleteAPIView.as_view(), name='delete-product'),

    # Sales
    path('sales/create/', views.SalesCreateAPIView.as_view(), name='create-sale'),
    path('sales/', views.SalesListAPIView.as_view(), name='list-sales'),
    path('sales/<str:pk>/details/', views.SalesRetrieveAPIView.as_view(), name='details-sale'),
    path('sales/<str:pk>/update/', views.SalesUpdateAPIView.as_view(), name='update-sale'),
    path('sales/<str:pk>/delete/', views.SalesDeleteAPIView.as_view(), name='delete-sale'),
    ]
