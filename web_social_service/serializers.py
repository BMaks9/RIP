from web_social_service.models import Patronage
from web_social_service.models import Disabilities
from web_social_service.models import Disabilities_Patronage
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
class GetPatronagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patronage
        # Поля, которые мы сериализуем
        fields = ["id","title", "img", "img_background", "deleted"]

class GetPatronagesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patronage
        # Поля, которые мы сериализуем
        fields = ["id","title", "description", "img", "img_background", "deleted"]

class GetDisabylitiesSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source = 'creator.username', read_only = True)
    # moderator = serializers.CharField(source = 'moderator.username', read_only = True)
    
    class Meta:
        # Модель, которую мы сериализуем
        model = Disabilities
        # Поля, которые мы сериализуем
        fields = ["id", "phone", "address", "status", "data_created", "data_compilation", "data_finished", "creator", "moderator"]
        
class GetDisabilities_Patronage_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Disabilities_Patronage
        # Поля, которые мы сериализуем
        fields = ["id","disabilities_id", "patronage_id", "comment"]

class GetDisabilitiesPatronageDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source = 'patronage_id.title')
    img = serializers.CharField(source = 'patronage_id.img')
    
    class Meta:
        model = Disabilities_Patronage
        # Поля, которые мы сериализуем
        fields = ["title", "img", "comment"]

class GetDisabilityDetail_Serializer(serializers.ModelSerializer):
    patronages = serializers.SerializerMethodField()
    def get_patronages(self, obj):
        patronages = Disabilities_Patronage.objects.filter(disabilities_id = obj.id)
        serializer = GetDisabilitiesPatronageDetailSerializer(patronages, many = True)
        return serializer.data
    class Meta:
        model = Disabilities
        fields = ['id', 'phone', 'address', 'patronages']