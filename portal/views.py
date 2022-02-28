from cgitb import lookup
from urllib import response
from django.db.models import Count, Sum
from pickle import TRUE
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from portal.models import Platform, Item, OrderItem, Seller, User
from portal.serializer import (
    SellerSerializer,
    OrderItemSerializer,
    ItemSerializer,
    PlatformSerializer,
    UserSerializer,
)


class GetItemView(APIView):
    def get(self, request):
        params = request.query_params
        platform_id = params.get("platform_id")
        if not platform_id:
            return Response({"error": "No platform id provided"}, status=400)

        order = (
            OrderItem.objects.filter(item__platform__id=platform_id[0])
            .values("item")
            .annotate(count=Count("item"))
            .order_by("count")
            .last()
        )
        return Response(
            {
                "count": order.get("count", 0),
                "item": ItemSerializer(
                    Item.objects.filter(id=order.get("item")).first()
                ).data,
            },
            status=200,
        )


class BestPlatformView(APIView):
    def get(self, request):
        params = request.query_params
        seller_id = params.get("seller_id")
        if not seller_id:
            return Response({"error": "No seller id provided"}, status=400)

        platform = (
            OrderItem.objects.filter(item__seller__id=seller_id)
            .values("platform")
            .annotate(sum=Sum("item__price"))
            .order_by("sum")
            .last()
        )
        return Response(
            {
                "total_price": platform.get("sum", 0),
                "platform": PlatformSerializer(
                    Platform.objects.filter(id=platform.get("platform")).first()
                ).data,
            },
            status=200,
        )


class BestPlatformForItemView(APIView):
    def get(self, request):
        params = request.query_params
        item_id = params.get("item_id")
        if not item_id:
            return Response({"error": "No platform id provided"}, status=400)
        platform = (
            OrderItem.objects.filter(item__id=item_id)
            .values("platform")
            .annotate(count=Count("platform"))
            .order_by("count")
            .last()
        )
        return Response(
            {
                "order_count": platform.get("count", 0),
                "item": PlatformSerializer(
                    Platform.objects.filter(id=platform.get("platform")).first()
                ).data,
            },
            status=200,
        )


class BestItemDateView(APIView):
    def get(self, request):
        params = request.query_params
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        if not start_date and end_date:
            return Response({"error": "No dates provided"}, status=400)

        item = OrderItem.objects.filter(
            order_date__gte=start_date, order_date__lte=end_date
        )

        return Response(
            {
                "item": OrderItemSerializer(item, many=True).data,
            },
            status=200,
        )


class UserlistView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin
):
    serializer_class = UserSerializer
    permission_class = [IsAuthenticated]
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(User, pk=kwargs["pk"])
        return Response(UserSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(UserSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


class SellerlistView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin
):
    serializer_class = SellerSerializer
    permission_class = [IsAuthenticated]
    queryset = Seller.objects.all()

    def get(self, request, *args, **kwargs):
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(Seller, pk=kwargs["pk"])
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
        ser = SellerSerializer(instance, data=request.data, partial=True)
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
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(Platform, pk=kwargs["pk"])
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
        ser = PlatformSerializer(instance, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=200)
        return Response(ser.errors, status=400)


class ItemlistView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin
):
    serializer_class = ItemSerializer
    permission_class = [IsAuthenticated]
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(Item, pk=kwargs["pk"])
        return Response(ItemSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(ItemSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk=None):
        return self.update(request, pk)


class OrderItemListView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin
):
    serializer_class = OrderItemSerializer
    permission_class = [IsAuthenticated]
    queryset = OrderItem.objects.all().order_by("-order_date")

    def post(self, request):
        data = request.data
        serializer = OrderItemSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(OrderItemSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, *args, **kwargs):
        return self.list(request)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)
