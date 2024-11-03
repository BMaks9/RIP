from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from datetime import date, datetime
from web_social_service.serializers import *
from web_social_service.models import Patronage, Disabilities, Disabilities_Patronage
from web_social_service.minio import add_pic, process_file_upload
from rest_framework.views import APIView
from rest_framework.decorators import api_view

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
            disability = Disabilities.objects.exclude(status = 'deleted').get(creator=request.user)
            list_patronage = Disabilities_Patronage.objects.filter(disabilities_id = disability.id)
            current_count = list_patronage.count()
            resp.append({'disabilities_id': disability.id, 'current_count': current_count})
        except:
            resp.append({'disabilities_id': None, 'current_count': None})
        
        return Response(resp)

    # Добавляет новую услугу
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
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
        patronage = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(patronage, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Удаляет информацию об акции
    def delete(self, request, id, format=None):
        patronage = get_object_or_404(self.model_class, id=id)
        patronage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# # Обновляет информацию об акции (для пользователя)    
# @api_view(['Put'])
# def put(self, request, pk, format=None):
#     stock = get_object_or_404(self.model_class, pk=pk)
#     serializer = self.serializer_class(stock, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatronageDraft(APIView):
    model_class = Disabilities_Patronage
    serializer_class = GetDisabilities_Patronage_Serializer

    def post(self, request, format=None):
        data = request.data.copy()
        try:
            disability = Disabilities.objects.exclude(status = 'deleted').get(creator=request.user)
        except:
            disability = Disabilities(status='draft', data_created = date.today(), creator=request.user)
            disability.save()
        data["disabilities_id"] = disability.id
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Возвращает информацию об услуге
class PatronageImage(APIView):
    model_class = Patronage
    serializer_class = GetPatronagesSerializer
    
    def post(self, request, id, format=None):    
        stock = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(stock, data=request.data, partial=True)
        # Изменение фото логотипа
        if 'pic' in serializer.initial_data:
            pic_result = add_pic(stock, serializer.initial_data['pic'])
            if 'error' in pic_result.data:
                return pic_result
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DisabilitiesList(APIView):
    model_class = Disabilities
    serializer_class = GetDisabylitiesSerializer

    # Возвращает список заявок
    def get(self, request, format=None):
        disabilities = self.model_class.objects.exclude(status__in = ['draft', 'deleted']).all()
        serializer = self.serializer_class(disabilities, many=True)
        resp = serializer.data        
        return Response(resp)
    
class DisabilitiesDetail(APIView):
    model_class = Disabilities
    serializer_class = GetDisabilityDetail_Serializer
    
    def get(self, request, id, format=None):
        disability = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(disability)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        disability = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(disability, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DisabilitiesSubmit(APIView):
    model_class = Disabilities
    serializer_class = GetDisabylitiesSerializer
    
    def put(self, request, id, format=None):
        data = request.data.copy()
        data['data_compilation'] = datetime.now()
        disability = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(disability, data= data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)