from web_social_service.models import Patronage
from web_social_service.models import Disabilities
from web_social_service.models import Disabilities_Patronage
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        
class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Неверные учетные данные")
        return {'user': user}

class GetPatronagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patronage
        # Поля, которые мы сериализуем
        fields = ["id","title", "img", "img_background"]

class GetPatronagesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patronage
        # Поля, которые мы сериализуем
        fields = ["id","title", "description", "img", "img_background"]

class GetDisabylitiesSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source = 'creator.username', read_only = True)
    moderator = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', required=False, allow_null=True)
    class Meta:
        # Модель, которую мы сериализуем
        model = Disabilities
        # Поля, которые мы сериализуем
        fields = ["id", "phone", "address", "status", "data_created", "data_compilation", "data_finished", 'date_dilivery',"creator", "moderator"]
        
class GetDisabilities_Patronage_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Disabilities_Patronage
        # Поля, которые мы сериализуем
        fields = ["id","disabilities_id", "patronage_id", "comment"]

class GetDisabilitiesPatronageDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source = 'patronage_id.id')
    title = serializers.CharField(source = 'patronage_id.title')
    img = serializers.CharField(source = 'patronage_id.img')
    
    class Meta:
        model = Disabilities_Patronage
        # Поля, которые мы сериализуем
        fields = ['id',"title", "img", "comment"]

class GetDisabilityDetail_Serializer(serializers.ModelSerializer):
    patronages = serializers.SerializerMethodField()
    def get_patronages(self, obj):
        patronages = Disabilities_Patronage.objects.filter(disabilities_id = obj.id)
        serializer = GetDisabilitiesPatronageDetailSerializer(patronages, many = True)
        return serializer.data
    class Meta:
        model = Disabilities
        fields = ['id', 'phone', 'address', 'status', 'data_created', 'data_compilation', 'data_finished', 'date_dilivery', 'patronages']