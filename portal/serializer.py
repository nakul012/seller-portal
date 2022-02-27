from rest_framework import serializers
from portal.models import *




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__' 


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = '__all__' 

        
        


class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = Platform
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'



class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'

        
