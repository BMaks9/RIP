from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from datetime import date, datetime
from web_social_service.serializers import *
from web_social_service.models import Patronage, Disabilities, Disabilities_Patronage
from web_social_service.minio import add_pic, process_file_upload, delete_image
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout

class PatronageList(APIView):
    model_class = Patronage
    serializer_class = GetPatronagesSerializer

    # Возвращает список услуг
    def get(self, request, format=None):
        patronages = self.model_class.objects.filter(deleted = 0).all()
        
        if 'patronageName' in request.GET:
            query = request.GET.get('patronageName')
            patronages = self.model_class.objects.filter(title__istartswith = query)
        serializer = self.serializer_class(patronages, many=True)
        resp = serializer.data
        try:
            disability = Disabilities.objects.get(status = 'draft', creator=request.user)
            list_patronage = Disabilities_Patronage.objects.filter(disabilities_id = disability.id)
            current_count = list_patronage.count()
            resp.append({'disabilities_id': disability.id, 'current_count': current_count})
        except:
            resp.append({'disabilities_id': None, 'current_count': None})
        
        return Response(resp)

    # Добавляет новую услугу (moderator) 
    def post(self, request, format=None):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = GetPatronagesDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatronageDetail(APIView):
    model_class = Patronage
    serializer_class = GetPatronagesDetailSerializer

    # Возвращает информацию об услуге
    def get(self, request, id, format=None):
        patronage = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(patronage)
        return Response(serializer.data)
    
    # Обновляет информацию об услуге (для модератора)
    def put(self, request, id, format=None):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        patronage = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(patronage, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Удаляет информацию об акции (moderator) + удаление изображения minio
    def delete(self, request, id, format=None):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        patronage = get_object_or_404(self.model_class, id=id)
        delete_image(patronage.img)
        patronage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PatronageDraft(APIView):
    model_class = Disabilities_Patronage
    serializer_class = GetDisabilities_Patronage_Serializer
    permission_classes = [IsAuthenticated]
    
    # формирование заявки (создатель)
    def post(self, request, id, format=None):
        try:
            disability = Disabilities.objects.get(status = 'draft', creator=request.user)
        except:
            disability = Disabilities(status='draft', data_created = date.today(), creator=request.user)
            disability.save()
        request.data["disabilities_id"] = disability.id
        request.data["patronage_id"] = id
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatronageImage(APIView):
    model_class = Patronage
    serializer_class = GetPatronagesSerializer
    
    def post(self, request, id, format=None):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        patronage = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(patronage, data=request.data, partial=True)
        # Изменение фото логотипа
        if 'pic' in serializer.initial_data:
            pic_result = add_pic(patronage, serializer.initial_data['pic'])
            if 'error' in pic_result.data:
                return pic_result
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DisabilitiesList(APIView):
    model_class = Disabilities
    serializer_class = GetDisabylitiesSerializer
    permission_classes = [IsAuthenticated]
    # Возвращает список заявок
    def get(self, request, format=None):
        status_filter = request.query_params.get('status', None)
        date_filter = request.query_params.get('data_compilation', None)
        
        disabilities = self.model_class.objects.exclude(status__in = ['draft', 'deleted']).filter(creator = request.user).all()
        
        if status_filter:
            disabilities = disabilities.filter(status = status_filter)
        if date_filter:
            disabilities = disabilities.filter(data_compilation = date_filter)
        serializer = self.serializer_class(disabilities, many=True)
        resp = serializer.data        
        return Response(resp)
    
class DisabilitiesDetail(APIView):
    model_class = Disabilities
    serializer_class = GetDisabilityDetail_Serializer
    permission_classes = [IsAuthenticated]
    #просмотр заявки 
    def get(self, request, id, format=None):
        disability = get_object_or_404(self.model_class.objects.exclude(status = 'deleted'), id=id)
        serializer = self.serializer_class(disability)
        return Response(serializer.data)
    #изменение заявки 
    def put(self, request, id, format=None):
        disability = get_object_or_404(self.model_class, id=id, status = 'draft')
        serializer = self.serializer_class(disability, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #удаление заявки
    def delete(self, request, id, format=None):
        data = request.data.copy()
        data['status'] = 'deleted'
        disability = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(disability, data= data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DisabilitiesSubmit(APIView):
    model_class = Disabilities
    serializer_class = GetDisabylitiesSerializer
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id, format=None):
        request.data['data_compilation'] = datetime.now()
        request.data['status'] = 'formed'
        disability = get_object_or_404(self.model_class, id=id, status = 'draft')
        serializer = self.serializer_class(disability, data= request.data, partial=True)
        if serializer.is_valid():
            disability_instance = serializer.save()
            if request.user.username != disability_instance.creator.username:
                return Response(status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DisabilitiesComplete(APIView):
    model_class = Disabilities
    serializer_class = GetDisabylitiesSerializer
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id, format=None):
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        
        request.data['data_finished'] = datetime.now()
        request.data['moderator'] = request.user.username
        action = request.GET.get('action')
        
        if action == 'completed':
            request.data['status'] = 'completed'
        elif action == 'rejected':
            request.data['status'] = 'rejected'
            
        disability = get_object_or_404(self.model_class, id=id, status = 'formed')
        serializer = self.serializer_class(disability, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Disabilities_Patronage_Edit(APIView):
    model_class = Disabilities_Patronage
    serializer_class = GetDisabilities_Patronage_Serializer
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, disabilityId, patronageId, format=None):
        disability_patronage = get_object_or_404(self.model_class, disabilities_id = disabilityId, patronage_id = patronageId)
        disability_patronage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, disabilityId, patronageId, format=None):
        disability_patronage = get_object_or_404(self.model_class, disabilities_id = disabilityId, patronage_id = patronageId)
        serializer = self.serializer_class(disability_patronage, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UsersReg(APIView):
    model_class = User
    serializer_class = UserSerializer
    
    def post(self, request, format=None):    
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UsersProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserUpdateSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersLogin(APIView):
    model_class = User
    serializer_class = UserAuthSerializer
    
    def post(self, request, format=None):    
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # Удаляем токен
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)