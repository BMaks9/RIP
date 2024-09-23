from django.shortcuts import render

data_application = {
                'id': 1,
                'phone': '79632277696',
                'address': 'Москва,ул.Уральская,д.10',
                'services':[{
                    'id' : 1,
                    'title' : 'Ногтевой сервис',
                    'img':'//127.0.0.1:9000/web-service/service1.jpg',
                    'comment': 'Заказываю ногтевой сервис для маломобильных родственников. Хочу, чтобы им было комфортно и уютно, как дома.',
                },
                {
                    'id' : 2,
                    'title' : 'Парикмахерские услуги',
                    'img':'//127.0.0.1:9000/web-service/service2.png',
                    'comment': 'Хочу немного изменить свой образ и почувствовать себя новой.',
                },
                {
                    'id' : 3,
                    'title' : 'Купание маломобильных',
                    'img':'//127.0.0.1:9000/web-service/service3.png',
                    'comment': 'Была бы благодарна, если вы предоставите услуги купания для моей маломобильной бабушки. Это ей очень поможет.',
                },
                ],
            }
data = {'services': [                
                {
                    'id' : 1,
                    'title' : 'Ногтевой сервис',
                    'description': 'Гигиенический парамедицинский аппаратный педикюр и маникюр комплексный (обработка стоп и ногтей до щиколотки) для пожилых, инвалидов, лежачих и маломобильных граждан, а также для людей с такими проблемами как: грибок, вросший ноготь, онихолизис (отслоение ногтевой пластины), гиперкератоз (трещины на стопах, сильные наросты огрубевшей кожи), натоптыши, все виды мозолей (в т.ч. стержневая). Услуга оказывается больным сахарным диабетом (диабетическая стопа), после инсульта, при гипертонусе мышц. Работаем с любой степенью запущенности. Устранение проблем "дохирургическими" методами.',
                    'img':'//127.0.0.1:9000/web-service/service1.jpg',
                    'img_background': '//127.0.0.1:9000/web-service/service-background1.png',
                },
                {
                    'id' : 2,
                    'title' : 'Парикмахерские услуги',
                    'description': 'Все виды парикмахерских услуг любой сложности для пожилых, инвалидов, лежачих и маломобильных граждан, в том числе для лиц старше 18 лет, желающих получить услугу парикмахера с выездом на дом. Наш спектр: все виды стрижек (классическая и модельная), окрашивания любой сложности, химическая завивка, бритьё и стрижка бороды и усов, окрашивание и коррекция бровей и ресниц.',
                    'img':'//127.0.0.1:9000/web-service/service2.png',
                    'img_background': '//127.0.0.1:9000/web-service/service-background2.png',
                },
                {
                    'id' : 3,
                    'title' : 'Купание маломобильных',
                    'description': 'Услугу оказывают специалисты, имеющие медицинское образование и многолетний опыт работы в сфере патронажного ухода. Санитары и медицинские сестры обладают уверенными и бережными навыками перемещения и позиционирования человека согласно принципам кинестетики. У бригады имеется все необходимое для того, чтобы купание было безопасным и приятным: специализированные сидения для фиксации подопечного, надувная ванночка для мытья головы, мягкие одноразовые мочалки, бритвенный станок, гипоаллергенная косметика, одноразовые впитывающие пеленки, увлажняющий крем для чувствительной сухой кожи, парикмахерские инструменты для стрижки волос и бороды. Вам нужно подготовить только чистое нательное и постельное белье и два мягких полотенца среднего размера.',
                    'img':'//127.0.0.1:9000/web-service/service3.png',
                    'img_background': '//127.0.0.1:9000/web-service/service-background3.png',
                },
                {
                    'id' : 4,
                    'title' : 'Уборка квартир',
                    'description': 'Стоимость наших услуг доступна и прозрачна. Цена за уборку квартиры и мытье окон варьируется в зависимости от объема работы, типа уборки и специфики объекта. Вы можете вызвать наших специалистов в удобное для вас время, и они оперативно приедут на указанный адрес, чтобы выполнить уборку. Обращаясь в компанию, вы получаете профессиональные услуги уборки квартиры и мытья окон с выездом на дом для пожилых, инвалидов, маломобильных и лежачих граждан в Москве и Московской области. Мы ценим ваше доверие и стремимся предоставить вам высококачественный сервис, который облегчит вашу жизнь и сделает ваш дом чистым и уютным.',
                    'img':'//127.0.0.1:9000/web-service/service4.jpg',
                    'img_background': '//127.0.0.1:9000/web-service/service-background4.png',
                },
                {
                    'id' : 5,
                    'title' : 'Психологическая помощь',
                    'description': 'Психологи нашей патронажной службы работают по следующим направлениям:боязнь принятия решений и проблема выбора; эмоциональная зависимость, боязнь разлуки – работа ведется как с парами, уже находящимися в разводе, так и с теми, кто не может решиться на серьезный шаг; подсознательные страхи, фобии, навязчивые негативные мысли; поиск партнера для создания семьи, работа с собственными недостатками и комплексами; низкая самооценка; неуверенность в себе; решение вопроса профессиональной нереализованности. Занятия ведутся как один на один с психологом, так и в группе из двух человек (например, супруги). Это позволяет индивидуально подойти к решению проблем и подобрать технику для каждого конкретного случая.',
                    'img':'//127.0.0.1:9000/web-service/service5.jpg',
                    'img_background': '//127.0.0.1:9000/web-service/service-background5.jpg',
                },
                {
                    'id' : 6,
                    'title' : 'Уход в стационаре',
                    'description': 'Помощник по уходу за больными в Москве – это возможность организовать лежачим пациентам профессиональную помощь, обеспечить присмотр и заботу в любое время суток. Сотрудники патронажной службы знают все нюансы ухода за больными в стационаре: быстро переоденут, поменяют белье, проведут гигиену тела, обработают кожу, своевременно дадут лекарства и вызовут лечащего врача при изменении самочувствия. Особенно актуален платный уход за пожилыми больными, часто страдающими психологическими и возрастными расстройствами. Только опытным патронажным сестрам под силу выполнять ухаживающие мероприятия, с которыми иногда не справляются даже заботливые родственники.',
                    'img':'//127.0.0.1:9000/web-service/service6.jpg',
                    'img_background': '//127.0.0.1:9000/web-service/service-background6.jpg',
                },
                {
                    'id' : 7,
                    'title' : 'Сопровождение пожилых',
                    'description': 'Сопровождение пожилых людей – услуга, которую оказывают сиделки, имеющие базовую подготовку, действующие в рамках законодательства РФ и искренне любящие свою работу. Задачи компаньонки: обеспечивать нормальные бытовые условия для подопечных; контролировать прием препаратов и выполнение процедур, назначенных лечащим врачом, содействовать восстановлению после болезни; организовывать досуг; поддерживать морально и физически; помогать адаптироваться в новых условиях, наладить общение; способствовать избавлению от вредных привычек, организация правильного питания; в экстренном случае оперативно связаться с родственниками или врачом.',
                    'img':'//127.0.0.1:9000/web-service/service7.jpg',
                    'img_background': '//127.0.0.1:9000/web-service/service-background7.jpg',
                },
                {
                    'id' : 8,
                    'title' : 'Патронажная сестра',
                    'description': 'Профессиональный патронаж – жизненная необходимость при невозможности для родственников самостоятельно ухаживать за своими старенькими уже родителями. Патронажная сестра (так называется специалист, занятый уходом за старичками на дому) помогает пациенту в выполнении самых разных дел. Она осуществляет: помощь в проведении предписанных медицинских и гигиенических процедур; наведение порядка и чистоты в квартире; приготовление еды, включая диетические блюда; оказание психологической помощи. Кроме того, этот специалист не забудет напомнить, что пора принять лекарства и просто поддержит нормальное, непринужденное общение.',
                    'img':'//127.0.0.1:9000/web-service/service8.jpg',
                    'img_background': '//127.0.0.1:9000/web-service/service-background8.jpg',
                },
            ],
        }
def GetOrders(request):
    current_count = len(data_application['services'])
    if 'serviceName' in request.GET:
        query = request.GET.get('serviceName')
        data_temp = [service for service in data['services'] if service['title'].lower().startswith(query.lower())]
        return render(request, 'services.html', {'data' : {'services': data_temp}, 'id_application': data_application['id'], 'current_count': current_count})
    return render(request, 'services.html', {'data' : data, 'id_application': data_application['id'], 'current_count': current_count})

def GetOrder(request, id):
    for service in data['services']:
        if service['id'] == id:
            data_temp = service
    return render(request, 'service.html', {'id': id, 'data' : data_temp})

def GetApplication(request, id):
    return render(request, 'application.html', {'id': id,  'data': data_application})