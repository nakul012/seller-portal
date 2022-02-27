from cgitb import lookup
from django.db.models import Max
from pickle import TRUE
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from portal.models import Platform, Item, OrderItem, Seller, User
from portal.serializer import SellerSerializer, OrderItemSerializer, ItemSerializer, PlatformSerializer, UserSerializer



class GetItemView(APIView):

    def get(self, request):
        params = request.query_params
        platform_id = params.get("platform_id")
        if not platform_id:
            return Response({"error": "No platform id provided"}, status=400)
        platform = get_object_or_404(Platform, pk=platform_id)

        order_item = OrderItem.objects.values('item').annotate(max_item=Max('item__platform')).order_by()



class UserlistView(generics.GenericAPIView, mixins.ListModelMixin,mixins.DestroyModelMixin ):
    serializer_class = UserSerializer
    permission_class = [IsAuthenticated]
    queryset = User.objects.all()


    def get(self, request, *args, **kwargs):
        #params = request.query_params
        if not 'pk' in kwargs:
            return self.list(request)
        post = get_object_or_404(User, pk=kwargs['pk'])
        return Response(UserSerializer(post).data, status=200)


    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(UserSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        return self.destroy(request, id)


class SellerlistView(generics.GenericAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin):
    serializer_class = SellerSerializer
    permission_class = [IsAuthenticated]
    queryset = Seller.objects.all()

    def get(self, request, *args, **kwargs):
        if not 'pk' in kwargs:
            return self.list(request)
        post = get_object_or_404(Seller, pk=kwargs['pk'])
        return Response(SellerlistView(post).data, status=200)


    def post(self, request):
        data = request.data
        serializer = SellerSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(SellerSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)


    def patch(self, request, pk=None):
        instance = self.get_object(pk)
        ser = SellerSerializer(instance, data=request.data, partial = True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=200)
        return Response(ser.errors, status=400)


    def delete(self, request):
        return self.destroy(request, id)

class PlatformlistView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = PlatformSerializer
    permission_class = [IsAuthenticated]
    queryset = Platform.objects.all()


    def get(self, request, *args, **kwargs):
        if not 'pk' in kwargs:
            return self.list(request)
        post = get_object_or_404(Platform, pk=kwargs['pk'])
        return Response(PlatformSerializer(post).data, status=200)


    def post(self, request):
        data = request.data
        serializer = PlatformSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(PlatformSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk=None):
        instance = self.get_object(pk)
        ser = PlatformSerializer(instance, data=request.data, partial = True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=200)
        return Response(ser.errors, status=400)


class ItemlistView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin):
    serializer_class = ItemSerializer
    permission_class = [IsAuthenticated]
    queryset = Item.objects.all()
    #lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        if not 'pk' in kwargs:
            return self.list(request)
        post = get_object_or_404(Item, pk=kwargs['pk'])
        return Response(ItemSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(ItemSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

    def put(self,request,pk=None):
        return self.update(request,pk)



class OrderItemListView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = OrderItemSerializer
    permission_class = [IsAuthenticated]
    queryset = OrderItem.objects.all().order_by('-order_date')


    def post(self, request):
        data = request.data
        serializer = OrderItemSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(OrderItemSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, *args, **kwargs):
        return self.list(request)




