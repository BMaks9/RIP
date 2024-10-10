from django.shortcuts import render
from web_social_service.models import Patronage, Disabilities, Disabilities_Patronage
   
data_disability = {
                'id': 1,
                'phone': '79632277696',
                'address': 'Москва,ул.Уральская,д.10',
                'list_patronage':[{
                    'id' : 1,
                    'title' : 'Ногтевой сервис',
                    'img':'//127.0.0.1:9000/social-system/patronage1.jpg',
                    'comment': 'Заказываю ногтевой сервис для маломобильных родственников. Хочу, чтобы им было комфортно и уютно, как дома.',
                },
                {
                    'id' : 2,
                    'title' : 'Парикмахерские услуги',
                    'img':'//127.0.0.1:9000/social-system/patronage2.png',
                    'comment': 'Хочу немного изменить свой образ и почувствовать себя новой.',
                },
                {
                    'id' : 3,
                    'title' : 'Купание маломобильных',
                    'img':'//127.0.0.1:9000/social-system/patronage3.png',
                    'comment': 'Была бы благодарна, если вы предоставите услуги купания для моей маломобильной бабушки. Это ей очень поможет.',
                },
                ],
            }

def GetListPatronage(request):
    data = Patronage.objects.all().values()
    current_count = len(data_disability['list_patronage'])
    if 'patronageName' in request.GET:
        query = request.GET.get('patronageName')
        data_temp = [patronage for patronage in data if patronage['title'].lower().startswith(query.lower())]
        return render(request, 'list_patronage.html', {'data' : {'list_patronage': data_temp}, 'id_disability': data_disability['id'], 'current_count': current_count})
    return render(request, 'list_patronage.html', {'data' : {'list_patronage': data}, 'id_disability': data_disability['id'], 'current_count': current_count})

def GetPatronage(request, id):
    data = Patronage.objects.all().values()
    for patronage in data:
        if patronage['id'] == id:
            data_temp = patronage
            break
    return render(request, 'patronage.html', {'id': id, 'data' : data_temp})

def GetDisability(request, disabiliti_id):
    data = Disabilities_Patronage.objects.filter(disabilities_id = disabiliti_id)
    return render(request, 'disability.html', {'id': disabiliti_id,  'data' : data})
