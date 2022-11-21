from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView
from .serializers import ProductSerializer , CustomerSerializer ,CollectionSerializer , OrderSerializer , ReviewSerializer , CartSerializer
from .models import Product , Customer , Collection , Order , Cart
#from django.db.models.aggregates import Configuration
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.db.models.aggregates import Count
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.decorators import action


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True)
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class CollectionViewSet(ModelViewSet):
    #queryset = Collection.objects.all()
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ReviewViewSet(ModelViewSet):
    serializer = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')


from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
