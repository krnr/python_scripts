# -*- coding: utf-8
import time, pickle
import sqlite3
import urllib, json
from sys import argv
from ConfigParser import ConfigParser as CP
import vk_api

script, AGE_FROM, AGE_TO = argv
SEX = 2 # мальчики
ITEMS = [{'id': 51946,'title': 'Астраханское речное училище (ВФ АРУ)'}, {'id': 344233,'title': 'Бизнес-гимназия при ВИБ'}, {'id': 1716657,'title': 'Вечерняя школа №17'}, {'id': 87761,'title': 'Вечерняя школа №5'}, {'id': 205724,'title': 'Гидромелиоративный техникум'}, {'id': 198019,'title': 'Гимназия «Исток»'}, {'id': 194957,'title': 'Гимназия «Эврика»'}, {'id': 295408,'title': 'Гимназия №1'}, {'id': 12004,'title': 'Гимназия №10'}, {'id': 9397,'title': 'Гимназия №11'}, {'id': 12166,'title': 'Гимназия №12'}, {'id': 4105,'title': 'Гимназия №13'}, {'id': 15942,'title': 'Гимназия №14'}, {'id': 55882,'title': 'Гимназия №15 (шк. 52)'}, {'id': 288791,'title': 'Гимназия №2'}, {'id': 326436,'title': 'Гимназия №24'}, {'id': 210514,'title': 'Гимназия №27'}, {'id': 55870,'title': 'Гимназия №3'}, {'id': 274757,'title': 'Гимназия №4'}, {'id': 43324,'title': 'Гимназия №5'}, {'id': 51728,'title': 'Гимназия №6'}, {'id': 312656,'title': 'Гимназия №7'}, {'id': 28598,'title': 'Гимназия №8'}, {'id': 43905,'title': 'Гимназия №9'}, {'id': 70431,'title': 'Детско-юношеская спортивная школа №10'}, {'id': 259351,'title': 'Детско-юношеская спортивная школа №16'}, {'id': 169872,'title': 'Детско-юношеская спортивная школа №18'}, {'id': 1745268,'title': 'Детско-юношеская спортивная школа №20'}, {'id': 74464,'title': 'Детско-юношеская спортивная школа №4'}, {'id': 199724,'title': 'Детско-юношеская спортивная школа олимпийского резерва'}, {'id': 155123,'title': 'Детско-юношеский центр'}, {'id': 1705591,'title': 'ДОСААФ'}, {'id': 96390,'title': 'Индустриальный техникум (ВИТ)'}, {'id': 206118,'title': 'Институт непрерывного образования ВолГАУ (бывш. ВГСХА)'}, {'id': 1723489,'title': 'Кадетский казачий корпус им. К. И. Недорубова'}, {'id': 243624,'title': 'Колледж «Экономикс»'}, {'id': 206594,'title': 'Колледж Академии бюджета и казначейства (АБиК) МФ РФ'}, {'id': 181445,'title': 'Колледж бизнеса (ВКБ)'}, {'id': 100130,'title': 'Колледж ВГИиК'}, {'id': 74710,'title': 'Колледж ВМИИ им. Серебрякова'}, {'id': 46538,'title': 'Колледж газа и нефти (ВКГН)'}, {'id': 256945,'title': 'Колледж потребительской кооперации (ВКПК)'}, {'id': 192484,'title': 'Колледж при ВолГМУ'}, {'id': 86214,'title': 'Колледж профессиональных технологий, экономики и права (ВГКПТЭиП)'}, {'id': 154940,'title': 'Колледж ресторанного бизнеса'}, {'id': 330424,'title': 'Колледж управления и новых технологий (ВГКУиНТ)'}, {'id': 153335,'title': 'Кооперативный техникум'}, {'id': 242392,'title': 'Кулинарное училище №60'}, {'id': 225469,'title': 'Лесотехнический колледж'}, {'id': 55159,'title': 'Лицей №1'}, {'id': 313521,'title': 'Лицей №10'}, {'id': 171060,'title': 'Лицей №2'}, {'id': 205448,'title': 'Лицей №28'}, {'id': 240633,'title': 'Лицей №3'}, {'id': 81901,'title': 'Лицей №32'}, {'id': 328699,'title': 'Лицей №4'}, {'id': 258608,'title': 'Лицей №5'}, {'id': 315631,'title': 'Лицей №6'}, {'id': 51883,'title': 'Лицей №7'}, {'id': 257934,'title': 'Лицей №8 «Олимпия»'}, {'id': 282134,'title': 'Лицей №9'}, {'id': 19007,'title': 'Лицей при ВолгГТУ'}, {'id': 379307,'title': 'Лицей-интернат «Лидер» (бывш. ВОСХЛ)'}, {'id': 161427,'title': 'Машиностроительный колледж'}, {'id': 179475,'title': 'Медико-экологический техникум (ВМЭТ)'}, {'id': 263520,'title': 'Медицинский колледж (бывш. Медицинский колледж №1, №2, №6, ВОМК)'}, {'id': 177575,'title': 'Металлургический техникум'}, {'id': 283951,'title': 'Механический техникум'}, {'id': 1463347,'title': 'Морская школа РОСТО'}, {'id': 61702,'title': 'Мужской педагогический профессиональный лицей (ВМПЛ)'}, {'id': 343340,'title': 'Музыкальная школа «Этос»'}, {'id': 250713,'title': 'Музыкальная школа №1'}, {'id': 163021,'title': 'Музыкальная школа №10'}, {'id': 58106,'title': 'Музыкальная школа №11'}, {'id': 204311,'title': 'Музыкальная школа №13'}, {'id': 71804,'title': 'Музыкальная школа №14'}, {'id': 22082,'title': 'Музыкальная школа №15'}, {'id': 163906,'title': 'Музыкальная школа №2'}, {'id': 236939,'title': 'Музыкальная школа №3'}, {'id': 21056,'title': 'Музыкальная школа №5'}, {'id': 207496,'title': 'Музыкальная школа №6'}, {'id': 68571,'title': 'Музыкальная школа №7'}, {'id': 113707,'title': 'Музыкальная школа №8'}, {'id': 68465,'title': 'Музыкальная школа №9'}, {'id': 290502,'title': 'Музыкальная школа при ВГИИК'}, {'id': 208717,'title': 'Музыкальная школа при ВМИИ им. П. А. Серебрякова'}, {'id': 311731,'title': 'Музыкальное педагогическое училище'}, {'id': 282090,'title': 'Нефтехимический вечерний техникум'}, {'id': 465189,'title': 'Октябрьский лицей'}, {'id': 123262,'title': 'Педагогический колледж №1'}, {'id': 80021,'title': 'Педагогический колледж №2'}, {'id': 680454,'title': 'Поволжский межрегиональный строительный колледж (ВФ ПГМСК)'}, {'id': 98699,'title': 'Политехнический колледж (ВПК)'}, {'id': 156237,'title': 'Промышленно-экономический колледж (ВПЭК)'}, {'id': 204595,'title': 'Профессионально-технический колледж (ВПТК, бывш. ПУ 34)'}, {'id': 230698,'title': 'Профессионально-техническое училище №10'}, {'id': 1127449,'title': 'Профессионально-техническое училище №12'}, {'id': 219664,'title': 'Профессионально-техническое училище №16'}, {'id': 254567,'title': 'Профессионально-техническое училище №19'}, {'id': 1292456,'title': 'Профессионально-техническое училище №21'}, {'id': 256448,'title': 'Профессионально-техническое училище №22'}, {'id': 243010,'title': 'Профессионально-техническое училище №25'}, {'id': 696715,'title': 'Профессионально-техническое училище №32'}, {'id': 158530,'title': 'Профессионально-техническое училище №37'}, {'id': 218630,'title': 'Профессионально-техническое училище №41'}, {'id': 188237,'title': 'Профессионально-техническое училище №54'}, {'id': 715134,'title': 'Профессиональное училище №11'}, {'id': 1727803,'title': 'Профессиональное училище №26'}, {'id': 262496,'title': 'Профессиональное училище №27'}, {'id': 974391,'title': 'Профессиональное училище №31'}, {'id': 184695,'title': 'Профессиональное училище №33'}, {'id': 1563752,'title': 'Профессиональное училище №36'}, {'id': 113235,'title': 'Профессиональное училище №47'}, {'id': 1675245,'title': 'Профессиональное училище №6'}, {'id': 313108,'title': 'Профессиональное училище №62'}, {'id': 90801,'title': 'Профессиональное училище речного флота №28'}, {'id': 87940,'title': 'Профессиональный лицей №59'}, {'id': 110081,'title': 'Русско-американская школа (РАШ)'}, {'id': 188644,'title': 'Сельскохозяйственный лицей (ВГСХЛ)'}, {'id': 71898,'title': 'Социально-педагогический колледж (ВСПК)'}, {'id': 330132,'title': 'Строительный техникум (ВСТ)'}, {'id': 107177,'title': 'Техникум железнодорожного транспорта (ВТЖТ)'}, {'id': 1464224,'title': 'Техникум железнодорожного транспорта и коммуникаций (бывш. Профессиональное училище №39)'}, {'id': 1721770,'title': 'Техникум кадровых ресурсов (ВПТКР)'}, {'id': 1751461,'title': 'Техникум нефтяного и газового машиностроения им. Героя советского Союза Николая Сердюкова'}, {'id': 346278,'title': 'Техникум связи'}, {'id': 244656,'title': 'Техникум советской торговли'}, {'id': 280714,'title': 'Техникум туризма и гостиничного сервиса'}, {'id': 127907,'title': 'Технический колледж'}, {'id': 63535,'title': 'Технологический колледж (ВТК)'}, {'id': 75619,'title': 'Торгово-экономический колледж (ВолТЭК)'}, {'id': 218488,'title': 'Училище №17'}, {'id': 218266,'title': 'Училище №29'}, {'id': 328431,'title': 'Училище №38'}, {'id': 169599,'title': 'Училище №8'}, {'id': 283810,'title': 'Училище информационных технологий'}, {'id': 1514255,'title': 'Училище искусств и культуры при ВГИИК'}, {'id': 97014,'title': 'Училище искусств им. Серебрякова'}, {'id': 190306,'title': 'Училище олимпийского резерва (ВУОР)'}, {'id': 76945,'title': 'Физико-математическая школа при ВолГУ'}, {'id': 81680,'title': 'Химико-технологический техникум (ВХТТ)'}, {'id': 1659189,'title': 'Центр иностранных языков «Reward»'}, {'id': 148626,'title': 'Центральная школа искусств при Институте искусств'}, {'id': 206905,'title': 'Частная интегрированная школа (ЧИШ)'}, {'id': 206738,'title': 'Школа «Благословение»'}, {'id': 184757,'title': 'Школа «Вайда»'}, {'id': 90775,'title': 'Школа «Виктория»'}, {'id': 110080,'title': 'Школа «Гармония-1»'}, {'id': 39585,'title': 'Школа «Гармония-Альфа»'}, {'id': 58197,'title': 'Школа «Гармония-М»'}, {'id': 179023,'title': 'Школа «Гармония»'}, {'id': 71579,'title': 'Школа «Интеллектуал»'}, {'id': 337510,'title': 'Школа «Интенсив» (при ВолГТУ)'}, {'id': 333931,'title': 'Школа «Квалитет»'}, {'id': 63348,'title': 'Школа «На семи ветрах»'}, {'id': 240508,'title': 'Школа «Наука» (при ВолГУ)'}, {'id': 72631,'title': 'Школа «Ор Авнер»'}, {'id': 63063,'title': 'Школа «Поколение»'}, {'id': 256421,'title': 'Школа «Развитие»'}, {'id': 66186,'title': 'Школа «Родник»'}, {'id': 344576,'title': 'Школа «Созвездие»'}, {'id': 138232,'title': 'Школа «Шанс»'}, {'id': 172849,'title': 'Школа «Янес»'}, {'id': 53649,'title': 'Школа №1'}, {'id': 56493,'title': 'Школа №10'}, {'id': 53033,'title': 'Школа №100'}, {'id': 266298,'title': 'Школа №101'}, {'id': 10605,'title': 'Школа №102'}, {'id': 278276,'title': 'Школа №103'}, {'id': 71098,'title': 'Школа №104'}, {'id': 39869,'title': 'Школа №105'}, {'id': 190930,'title': 'Школа №106'}, {'id': 64631,'title': 'Школа №107'}, {'id': 167846,'title': 'Школа №108'}, {'id': 13919,'title': 'Школа №109'}, {'id': 59135,'title': 'Школа №11'}, {'id': 21200,'title': 'Школа №110'}, {'id': 29143,'title': 'Школа №111'}, {'id': 30126,'title': 'Школа №112'}, {'id': 28199,'title': 'Школа №113'}, {'id': 17970,'title': 'Школа №115'}, {'id': 75709,'title': 'Школа №116'}, {'id': 54299,'title': 'Школа №117'}, {'id': 39407,'title': 'Школа №118'}, {'id': 114575,'title': 'Школа №119'}, {'id': 113814,'title': 'Школа №12'}, {'id': 48400,'title': 'Школа №120'}, {'id': 76208,'title': 'Школа №121'}, {'id': 64632,'title': 'Школа №122'}, {'id': 82454,'title': 'Школа №123'}, {'id': 172273,'title': 'Школа №124'}, {'id': 52686,'title': 'Школа №125'}, {'id': 75793,'title': 'Школа №126'}, {'id': 114956,'title': 'Школа №127'}, {'id': 31170,'title': 'Школа №128'}, {'id': 18182,'title': 'Школа №129'}, {'id': 62142,'title': 'Школа №13'}, {'id': 15550,'title': 'Школа №130'}, {'id': 73799,'title': 'Школа №131'}, {'id': 15929,'title': 'Школа №132'}, {'id': 20963,'title': 'Школа №133'}, {'id': 45447,'title': 'Школа №134'}, {'id': 99209,'title': 'Школа №136'}, {'id': 179715,'title': 'Школа №139'}, {'id': 123560,'title': 'Школа №14'}, {'id': 17929,'title': 'Школа №140'}, {'id': 216029,'title': 'Школа №141'}, {'id': 34861,'title': 'Школа №15'}, {'id': 11121,'title': 'Школа №16'}, {'id': 54303,'title': 'Школа №17'}, {'id': 30980,'title': 'Школа №18'}, {'id': 5404,'title': 'Школа №19'}, {'id': 235093,'title': 'Школа №2'}, {'id': 2357,'title': 'Школа №20'}, {'id': 16916,'title': 'Школа №21'}, {'id': 98700,'title': 'Школа №22'}, {'id': 47238,'title': 'Школа №23'}, {'id': 3088,'title': 'Школа №24'}, {'id': 97827,'title': 'Школа №25'}, {'id': 83348,'title': 'Школа №26'}, {'id': 20260,'title': 'Школа №27'}, {'id': 44258,'title': 'Школа №28'}, {'id': 22659,'title': 'Школа №29'}, {'id': 45430,'title': 'Школа №3'}, {'id': 208375,'title': 'Школа №30'}, {'id': 20123,'title': 'Школа №31'}, {'id': 1678593,'title': 'Школа №32'}, {'id': 197107,'title': 'Школа №33'}, {'id': 24800,'title': 'Школа №34'}, {'id': 24044,'title': 'Школа №35'}, {'id': 40565,'title': 'Школа №36'}, {'id': 44743,'title': 'Школа №37'}, {'id': 47930,'title': 'Школа №38'}, {'id': 50228,'title': 'Школа №384'}, {'id': 169462,'title': 'Школа №39'}, {'id': 201903,'title': 'Школа №4'}, {'id': 21250,'title': 'Школа №40'}, {'id': 49373,'title': 'Школа №41'}, {'id': 161392,'title': 'Школа №42'}, {'id': 23799,'title': 'Школа №43'}, {'id': 18694,'title': 'Школа №44'}, {'id': 18708,'title': 'Школа №45'}, {'id': 185637,'title': 'Школа №46'}, {'id': 11782,'title': 'Школа №48'}, {'id': 46439,'title': 'Школа №49'}, {'id': 52647,'title': 'Школа №5'}, {'id': 5216,'title': 'Школа №50'}, {'id': 56096,'title': 'Школа №51'}, {'id': 168801,'title': 'Школа №53'}, {'id': 42,'title': 'Школа №54'}, {'id': 86187,'title': 'Школа №55'}, {'id': 718,'title': 'Школа №56'}, {'id': 6746,'title': 'Школа №57'}, {'id': 96357,'title': 'Школа №58'}, {'id': 68624,'title': 'Школа №59'}, {'id': 47067,'title': 'Школа №6'}, {'id': 67095,'title': 'Школа №60'}, {'id': 24545,'title': 'Школа №61'}, {'id': 51687,'title': 'Школа №62'}, {'id': 155036,'title': 'Школа №63'}, {'id': 52685,'title': 'Школа №64'}, {'id': 17543,'title': 'Школа №65'}, {'id': 91531,'title': 'Школа №66'}, {'id': 49074,'title': 'Школа №67'}, {'id': 89401,'title': 'Школа №68'}, {'id': 112196,'title': 'Школа №69'}, {'id': 338612,'title': 'Школа №7'}, {'id': 64995,'title': 'Школа №70'}, {'id': 15394,'title': 'Школа №71'}, {'id': 50834,'title': 'Школа №72'}, {'id': 44651,'title': 'Школа №73'}, {'id': 22095,'title': 'Школа №74'}, {'id': 51525,'title': 'Школа №75'}, {'id': 101220,'title': 'Школа №76'}, {'id': 5262,'title': 'Школа №77'}, {'id': 288070,'title': 'Школа №78'}, {'id': 86669,'title': 'Школа №79'}, {'id': 235741,'title': 'Школа №8'}, {'id': 213053,'title': 'Школа №80'}, {'id': 45,'title': 'Школа №81'}, {'id': 328247,'title': 'Школа №82'}, {'id': 19603,'title': 'Школа №83'}, {'id': 10968,'title': 'Школа №84'}, {'id': 246707,'title': 'Школа №85'}, {'id': 43828,'title': 'Школа №86'}, {'id': 93662,'title': 'Школа №87'}, {'id': 6899,'title': 'Школа №88'}, {'id': 63508,'title': 'Школа №89'}, {'id': 54433,'title': 'Школа №9'}, {'id': 226983,'title': 'Школа №90'}, {'id': 81256,'title': 'Школа №91'}, {'id': 26335,'title': 'Школа №92'}, {'id': 7818,'title': 'Школа №93'}, {'id': 31491,'title': 'Школа №94'}, {'id': 35455,'title': 'Школа №95'}, {'id': 21,'title': 'Школа №96'}, {'id': 25755,'title': 'Школа №97'}, {'id': 50676,'title': 'Школа №98'}, {'id': 15451,'title': 'Школа №99'}, {'id': 169137,'title': 'Школа-интернат №1'}, {'id': 156402,'title': 'Школа-интернат №2'}, {'id': 87762,'title': 'Школа-интернат №6'}, {'id': 9987,'title': 'Школа-интернат №7'}, {'id': 1486428,'title': 'Школа-интернат №8'}, {'id': 344968,'title': 'Школа-интернат №9'}, {'id': 138020,'title': 'Экономико-технический колледж (ВГЭТК)'}, {'id': 163448,'title': 'Энергетический колледж (ВЭК)'}, {'id': 99628,'title': 'Юридический лицей'}]
CHUNKS = [ITEMS[i:i+20] for i in range(0, len(ITEMS), 20)]

conn = sqlite3.connect('vk_schoolboys.sqlite')
DB = conn.cursor()

#DB.execute('''
#    CREATE TABLE Schoolboys (id INTEGER, first_name TEXT, last_name TEXT, 
#    screen_name TEXT, sex INTEGER, school_name TEXT, school_id TEXT)''')

def main():
    conf = CP()
    conf.read('vk_settings.ini')
    login, password = conf.get('Settings', 'Login'), conf.get('Settings', 'Password')
    global vk
    vk = vk_api.VkApi(login, password)

    try:
        vk.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return

    #tools = vk_api.VkTools(vk)    

    print "Searching ", AGE_FROM
    # what shall we look for?
    data = {
        'fields': 'screen_name,schools,sex,last_seen',
        'city': 10,
        'age_from': int(AGE_FROM),
        'age_to': int(AGE_TO),
        'count': 1000,
        'sex': SEX,
        'v': '5.41',
        }
    
    for chunk in CHUNKS:
        # use execute to get data, because 'users.search' has restictions on 1000 ids
        # params: chunk - list of dict's with school ids, data - json search
        users = execute(chunk, data)

        # use vk_api method to get data
        # users = tools.get_all('users.search', 100, data)
        # making dump. just in case smth will be wrong
        with open('dump.txt', 'a') as fh:
            pickle.dump(users, fh)
            fh.close()

        print 'Is there an error? or we\'ve retrieved %r users' % len(users)
        # if we got something let's put it into db 
        if len(users) > 0:
            for user in users:
                put_into_db(user)
        print 'Sleeping now...'
        time.sleep(180)
    # we've finished parsing, time to close db
    conn.close()

def execute(chunk, param_json):
    school_list = []
    # find ids from chunk dictionary
    for school in chunk:
        school_list.append(school['id'])
    code = '''var result = 0; 
    var items = []; 
    var schools={}; 
    while (schools.length > 0) {{
        var school_num = schools.pop();
        var data = {} + {{school: school_num}};
        var users = API.users.search(data); 
        result = result + users.count; 
        items = items + users.items; 
    }}; 
    return items;'''.format(school_list, json.dumps(param_json))
    print code
    # execute must return 'items' - list of ids dicts
    return vk.method('execute', {'code': code})

def put_into_db(user):
    # it takes an object from 'items' [..] api response as a parameter
    # and returns nothing, but makes a commit
    school_name, school_id = '',''
    # let's check whether a user is already in the database
    DB.execute('SELECT id FROM Schoolboys WHERE id = ?', (user['id'],))
    row = DB.fetchone()
    if row is None:
        # user is not in the db, trying to commit him
        # not every user have schools, so check if there's the last one
        try:
            school_name, school_id = user['schools'][-1]['name'], user['schools'][-1]['id']
        except Exception, e:
            # if there's no 'school' in 'user' just pass for now
            print "USER %s %s have no school stated!" % (user['first_name'], user['last_name'])
        finally:
            DB.execute('''INSERT INTO Schoolboys (id, first_name, last_name, screen_name, 
            sex, school_name, school_id, last_seen) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user['id'], user['first_name'], user['last_name'], user['screen_name'], user['sex'], school_name, school_id, user['last_seen']['time'], ))
    else:
        print "We already have this user!"
    conn.commit()

if __name__ == '__main__':
    main()