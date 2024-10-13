from django.shortcuts import render
from web_social_service.models import Patronage, Disabilities, Disabilities_Patronage
from datetime import date
from django.db import connection

def GetListPatronage(request):
    data = Patronage.objects.all()
    
    if 'del_button' in request.POST:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE \"Disabilities\" SET status = 'deleted' WHERE id = %s", [request.POST.get('del_button')])
    
    try:
        data_disability = Disabilities.objects.exclude(status = 'deleted').get(creator=request.user)
        list_patronage = Disabilities_Patronage.objects.filter(disabilities_id = data_disability)
        current_count = list_patronage.count()

    except:
        data_disability = None
        list_patronage = None
        current_count = 0
        
    if 'button_add_patronage' in request.POST:
        query = request.POST.get('button_add_patronage')
        if not(data_disability):
            data_disability = Disabilities(status='draft', data_created = date.today(), creator=request.user)
            data_disability.save()
        try:
            list_patronage.get(patronage_id = query)
        except:
            lst = Disabilities_Patronage(disabilities_id = data_disability, patronage_id = data.get(id = query))
            lst.save()
            current_count+=1
            
    if 'patronageName' in request.GET:
        query = request.GET.get('patronageName')
        data_filter = data.filter(title__istartswith = query)
        return render(request, 'list_patronage.html', {'data' : data_filter, 'disability': data_disability, 'current_count': current_count})
    
    return render(request, 'list_patronage.html', {'data' : data, 'disability': data_disability, 'current_count': current_count})

def GetPatronage(request, id):
    data = Patronage.objects.all().values()
    for patronage in data:
        if patronage['id'] == id:
            data_temp = patronage
            break
    return render(request, 'patronage.html', {'id': id, 'data' : data_temp})

def GetDisability(request, disabiliti_id):
    data = Disabilities_Patronage.objects.filter(disabilities_id = disabiliti_id).exclude(disabilities_id__status__icontains = 'deleted')
    return render(request, 'disability.html', {'id': disabiliti_id,  'data' : data})
