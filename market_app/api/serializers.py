from rest_framework import serializers
from django.contrib.auth.models import User
from market_app.models import Profiles, Offers, OffersDetails, Orders, Reviews
from django.db.models import Avg



### Offers ### _________________________________________________________________________

class OffersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffersDetails
        exclude = ['offer']

class OffersSerializer(serializers.ModelSerializer):
    details = OffersDetailSerializer(many=True)
    username = serializers.CharField(source='user.user.username', read_only=True)
    class Meta:
        model = Offers
        fields = '__all__'

    def update(self, instance, validated_data):
        all_prices = []
        all_dates = []
        new_details = validated_data.pop('details', None)
        if new_details:
            instance.details.all().delete()
            for details_data in new_details:
                all_prices.append(details_data["price"])
                all_dates.append(details_data["delivery_time_in_days"])
                instance.details.create(**details_data)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.min_price = min(all_prices, default=0)
        instance.min_delivery_time = min(all_dates, default=0)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['min_price'] = instance.min_price
        representation['min_delivery_time'] = instance.min_delivery_time
        return representation


class CreateOffersSerializer(serializers.ModelSerializer):
    details = OffersDetailSerializer(many=True)

    class Meta:
        model = Offers
        fields = '__all__'
        read_only_fields = ['user', 'min_price', 'min_delivery_time']

    
    def manipulate_validated_data(self, details):
        all_prices = []
        all_dates = []
        for each_detail in details:
            all_prices.append(each_detail["price"])
            all_dates.append(each_detail["delivery_time_in_days"])
        min_price = min(all_prices, default=0)
        min_date = min (all_dates, default=0)
        return (min_price, min_date)


    def create(self, validated_data): 
        request = self.context.get('request')

        if "details" not in validated_data:
            raise serializers.ValidationError({"details": "details are empty and required."})
        details_list = validated_data.pop('details', [])

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError({"User": "You must be logged in to create an offer."})
        
        profile = Profiles.objects.get(user=request.user)
        validated_data['user'] = profile
        validated_data['min_price'], validated_data['min_delivery_time'] = self.manipulate_validated_data(details_list)

        new_offer = Offers.objects.create(**validated_data) 
 
        for each_detail in details_list:
            each_detail["offer"] = new_offer
            OffersDetails.objects.create(**each_detail)

        return new_offer
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['min_price'] = instance.min_price
        representation['min_delivery_time'] = instance.min_delivery_time
        return representation



    

### Profiles ### _______________________________________________________________________

class ProfilesSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    date_joined = serializers.DateTimeField(source="user.date_joined", format="%Y-%m-%dT%H:%M:%SZ")

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for key, value in user_data.items():
            setattr(user, key, value)
        user.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance

    class Meta():
        model = Profiles
        exclude = []


class UserSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source="id")

    class Meta:
        model = User
        fields = ["pk", "username", "first_name", "last_name"]

class ProfilesTypeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta():
        model = Profiles
        exclude = []


### Orders ### _______________________________________________________________________

class OrdersSerializer(serializers.ModelSerializer):
    offersDetails = OffersDetailSerializer(read_only=True)
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta():
        model = Orders
        exclude = []
        read_only_fields = ['user', 'offersDetails', 'status']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        profil = Profiles.objects.get(user=user)
        offer_detail_id = request.data.get("offer_detail_id")
        if not user or not user.is_authenticated:
            raise serializers.ValidationError({"User":"You have to sign in to make an order."})
        if not offer_detail_id:
            raise serializers.ValidationError({"OrderDetail": "Id of your Order can't be found."})
        order_detail = OffersDetails.objects.get(pk=offer_detail_id)
        new_order = Orders.objects.create(user=profil, offersDetails=order_detail, status="in_progress")
        return new_order
    
    def update(self, instance, validated_data):
        request = self.context['request']
        status = request.data.get('status')
        instance.status = status
        instance.save()
        return instance
    
    def to_representation(self, instance):
        instance_view = super().to_representation(instance)
        user = instance_view.pop('user')
        business_user_id = instance.offersDetails.offer.user.id
        customer_view= {
            'customer_user': user,
            'business_user' : business_user_id
        }
        offers_view = instance_view.pop('offersDetails', {})
        offers_view.pop('id', {})
        return {**instance_view, **offers_view, **customer_view}

        
### Reviews ### _______________________________________________________________________

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta():
        model = Reviews
        exclude = []
        read_only_fields = ['reviewer']

    def create(self, validated_data):
        request = self.context['request']
        if not request or not request.user:
            raise serializers.ValidationError({'error': "You must be logged in to create a Review."})

        profil = Profiles.objects.get(user=request.user)
        validated_data['reviewer'] = profil
        review = Reviews.objects.create(**validated_data)
        return review

### Base-info ### _______________________________________________________________________


class OrderCountSerializer(serializers.Serializer):
    class OrderCountSerializer(serializers.Serializer):
        order_count = serializers.IntegerField()

    def to_representation(self, instance):
        pk = self.context.get('pk')
        profil = Profiles.objects.get(user=pk)
        if profil.type != 'business' or not profil:
             raise serializers.ValidationError({'error': 'Business user not found.'})
        order_count = Orders.objects.filter(offersDetails__offer__user=profil, status='in_progress').count()
        return {'order_count': order_count}
    
class completedOrderCountSerializer(serializers.Serializer):
    class OrderCountSerializer(serializers.Serializer):
        completed_order_count = serializers.IntegerField()

    def to_representation(self, instance):
        pk = self.context.get('pk')
        profil = Profiles.objects.get(user=pk)
        if profil.type != 'business' or not profil:
             raise serializers.ValidationError({'error': 'Business user not found.'})
        completed_order_count = Orders.objects.filter(offersDetails__offer__user=profil, status='completed').count()
        return {'completed_order_count': completed_order_count}


class BaseInfoSerializer(serializers.Serializer):
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    business_profile_count = serializers.SerializerMethodField()
    offer_count = serializers.SerializerMethodField()

    def get_review_count(self, obj):
        return Reviews.objects.count()
    
    def get_offer_count(self, obj):
        return Offers.objects.count()

    def get_business_profile_count(self, obj):
        return Profiles.objects.filter(type='business').count()
    
    def get_average_rating(self, obj):
        average = Reviews.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(average, 1) if average is not None else 0.0

    