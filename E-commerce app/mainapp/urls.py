from django.urls import path
from .views import ProductViewSet , CustomerViewSet , OrderViewSet , CollectionViewSet
from django.urls.conf import include
from rest_framework_nested import routers
from .import views


router = routers.DefaultRouter()
router.register('products' , views.ProductViewSet, basename='products')
router.register('collections' , views.CollectionViewSet , basename= 'collections')
router.register('orders' , views.OrderViewSet, basename= 'orders')
router.register('customers' , views.CustomerViewSet , basename = 'customers')
router.register('carts', views.CartViewSet)

products_router = routers.NestedDefaultRouter(router, 'products' , lookup='product')
products_router.register('reviews' , views.ReviewViewSet , basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = router.urls + products_router.urls + carts_router.urls

'''urlpatterns = [
    path('product/', ProductViewSet.as_view()),
    path('customer/', CustomerViewSet.as_view()),
    path('order/', OrderViewSet.as_view()),
    path('collection/', CollectionViewSet.as_view())
]'''