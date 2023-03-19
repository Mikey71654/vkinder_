from dataclasses import dataclass
from pprint import pprint
from sql_db import register_user, check_db_reg, list_favorite, delete_db_elit, add_user, check_db_user
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from vk_func import search_users, get_photo

my_token = 'vk1.a.oTI4wyPkUNx3n7EeWBl-3uJ_3XBk8puHJ7eXUeH_jh4pE7QKYBYAGwH46B_1nKv9FNUihK1SjAMvHiovFWZ7DKWRpBByWXHrI9CWDbyoSwfLZAjhgWX660v1lx_5jRVVn3ws6qz8fNcbWKuVihQZpJbfCQBii2Spr5VJRAW3xppetXE-XXGMn-TtKtOLMTGnmcp-w3dnm9zUniUFdztxzA'
group_token = 'vk1.a.j3dPowsPmxhGrUbQbGvR4akT90Actz4SGW80FkVAqCGMHxGtAIdGU2kp49wBF7Zzf_V7eszpOsnPjbNHPd3-j3DyDXSnD1lnPijGnKDaQM4osi26BoTt6WnfDgFjNZzOwx5plkhclTqdJduTfNgIAFtSCdsW2IK6vVCSGFYWBKyzH342_DRZjBfLbnl3zLN3ykTEGGMtwJWGFNma1Cgm2Q'
vk_session = vk_api.VkApi(token=group_token)
session = vk_api.VkApi(token=my_token)
group_id = '-21842051'
longpoll = VkLongPoll(vk_session)
n = 0


@dataclass
class MsgBot:
    misunderstand = 'Не понимаю о чём вы..'
    start = 'Привет! Начнем поиск? Или посмотрим кто у нас уже есть?'
    criterions = 'Выберите критерии поиска'
    again = 'Начнём сначала?'
    minage = 'Введите минимальный возраст'
    maxage = 'Введите максимальный возраст'
    sex = 'Выберите пол'
    greetings = ['привет', 'приветик', 'хай', 'ку', 'hello', 'start', 'goodbye']
    leav = ['пока', 'конец', 'не хочу больше искать']
    gd = 'Пока!'
    city = 'Введите название города'
    city_error = 'Такого города нет'
    boy = 'Выбраны мальчики'
    girl = 'Выбраны девочки'


class VkBot():

    def send_msg(user_id, message, keyboard=None):
        params = {'user_id': user_id,
                  'message': message,
                  'random_id': randrange(10**5)}

        if keyboard != None:
            params['keyboard'] = keyboard.get_keyboard()

        vk_session.method('messages.send', params)

    print("Server started")

    def set_keyboard_start(self):
        keyboard = VkKeyboard()
        keyboard.add_button('Задать критерии', VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Посмотреть избранное', VkKeyboardColor.PRIMARY)
        return keyboard

    def set_search_keyboard(self):
        keyboard = VkKeyboard()
        keyboard.add_button('Выбрать город', VkKeyboardColor.PRIMARY)
        keyboard.add_button('Выбрать пол', VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Возраст', VkKeyboardColor.PRIMARY)
        keyboard.add_button('Поиск!', VkKeyboardColor.PRIMARY)
        keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
        return keyboard

    def sex_keyboard(self):
        keyboard = VkKeyboard()
        keyboard.add_button('ОН', VkKeyboardColor.PRIMARY)
        keyboard.add_button('ОНА', VkKeyboardColor.PRIMARY)
        keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
        return keyboard

    def elit_keyboard(self):
        keyboard = VkKeyboard()
        keyboard.add_button('Удалить', VkKeyboardColor.PRIMARY)
        keyboard.add_button('Следующее', VkKeyboardColor.PRIMARY)
        keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
        return keyboard

    def set_found_keyboard(self):
        keyboard = VkKeyboard()
        keyboard.add_button('В избранное', VkKeyboardColor.PRIMARY)
        keyboard.add_button('Следующее', VkKeyboardColor.PRIMARY)
        keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
        return keyboard

    def get_city_id(self, user_id):
        VkBot.send_msg(user_id, MsgBot.city, self.set_search_keyboard())
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                city = event.text
                VkBot.send_msg(user_id, f'Выбран город {city}')
                return city

    def get_sex(self, user_id):
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text.lower()

                if text == 'он':
                    VkBot.send_msg(user_id, MsgBot.boy, self.set_search_keyboard())
                    return 2

                if text == 'она':
                    VkBot.send_msg(user_id, MsgBot.girl, self.set_search_keyboard())
                    return 1

                if text == 'назад' or text == 'Назад':
                    VkBot.send_msg(user_id, 'Начнём сначала', self.set_keyboard_start())
                    self.starting()

    def found(self, user_id, hometown, sex, age):
        global n
        list_of_users = search_users(sex, age, hometown)
        pprint(list_of_users)
        if n != len(list_of_users):
            photo_ = get_photo(list_of_users[n][3])

            if len(list_of_users) > 0 and photo_ != 'в доступе к фото отказано':

                VkBot.send_msg(user_id, f'{list_of_users[n][0]} {list_of_users[n][1]} \n {list_of_users[n][2]}')

                photo = "photo{}_{}".format(get_photo(int(list_of_users[n][3]))['owner_id'],
                                            get_photo(int(list_of_users[n][3]))['photo_id'])
                vk_session.method("messages.send", {'peer_id': user_id, 'attachment': photo, "random_id": randrange(10**5)})

                n += 1

            elif len(list_of_users) > 0 and photo_ == 'в доступе к фото отказано':

                VkBot.send_msg(user_id, f'{list_of_users[n][0]} {list_of_users[n][1]} \n {list_of_users[n][2]} '
                                        f'\n"Закрытый профиль или нет фото"')
                n += 1

            elif len(list_of_users) == 0:
                VkBot.send_msg(user_id, f'Людей с такими параметрами нет')

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    text = event.text.lower()

                    if text == 'следующее' and n != len(list_of_users):

                        photo_ = get_photo(list_of_users[n][3])

                        if len(list_of_users) > 0 and photo_ != 'в доступе к фото отказано' and n != len(list_of_users):

                            VkBot.send_msg(user_id, f'{list_of_users[n][0]} {list_of_users[n][1]} \n {list_of_users[n][2]}')

                            photo = "photo{}_{}".format(get_photo(int(list_of_users[n][3]))['owner_id'],
                                                        get_photo(int(list_of_users[n][3]))['photo_id'])
                            print(type(photo))
                            vk_session.method("messages.send",
                                              {'peer_id': user_id, 'attachment': photo, "random_id": randrange(10 ** 5)})
                            n += 1

                        elif len(list_of_users) > 0 and photo_ == 'в доступе к фото отказано' and n != len(list_of_users):
                            VkBot.send_msg(user_id, f'{list_of_users[n][0]} {list_of_users[n][1]} \n {list_of_users[n][2]}')
                            VkBot.send_msg(user_id, f'Фото нет или закрытый профиль')
                            n += 1

                        elif n == len(list_of_users):

                            VkBot.send_msg(user_id, f'Кандидаты закончились, введите новые параметры')

                    if text == 'в избранное' and check_db_user(list_of_users[n-1][3]) is None:

                        photo_ = get_photo(list_of_users[n-1][3])

                        if len(list_of_users) > 0 and photo_ != 'в доступе к фото отказано':

                            photo = "photo{}_{}".format(get_photo(int(list_of_users[n-1][3]))['owner_id'],
                                                        get_photo(int(list_of_users[n-1][3]))['photo_id'])
                            add_user(vk_id=list_of_users[n-1][3],
                                     name=list_of_users[n-1][0],
                                     surname=list_of_users[n-1][1],
                                     link=list_of_users[n-1][2],
                                     gender=sex,
                                     year=age,
                                     city=hometown,
                                     id_user=user_id,
                                     photo=photo)
                            VkBot.send_msg(user_id, f'Добавлен в избранное')

                        else:
                            VkBot.send_msg(user_id, f'Вы не можете добавить пользователя, у которого нет фото или закрытый профиль')

                    elif text == 'в избранное' and check_db_user(list_of_users[n-1][3]) is not None:
                        VkBot.send_msg(user_id, f'Уже в избранном')



                    elif n == len(list_of_users):
                        VkBot.send_msg(user_id, f'Кандидаты закончились, введите новые параметры')


                    if text == 'назад':
                        VkBot.send_msg(user_id, 'Начнём сначала', self.set_keyboard_start())
                        n = 0
                        self.starting()
        else:
            VkBot.send_msg(user_id, f'Кандидаты закончились, введите новые параметры')

    def get_age(self, user_id):
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text.lower()
                if text.isdigit() and int(text) >= 14 and int(text) <= 200:
                    VkBot.send_msg(user_id, f'Возраст {text} лет')
                    return int(text)

                else:
                    VkBot.send_msg(user_id, f'Вы неправильно ввели параметры')
                    self.set_search_params(user_id)

    def set_search_params(self, user_id):
        dict_ = {}
        sex_ = ''
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text.lower()

                if text == 'назад' or text == 'Назад':
                    VkBot.send_msg(user_id, 'Начнём сначала', self.set_keyboard_start())
                    self.starting()

                elif text == 'выбрать город':
                    dict_['hometown'] = self.get_city_id(user_id)
                    print(dict_)

                elif text == 'выбрать пол':
                    VkBot.send_msg(user_id, 'Мальчики или девочки?', self.sex_keyboard())
                    dict_['sex'] = self.get_sex(user_id)
                    print(dict_)

                elif text == 'поиск!':
                    if len(dict_) == 3:

                        VkBot.send_msg(user_id, 'Будем искать по тем критериям, которые вы задали', self.set_found_keyboard())
                        self.found(user_id, dict_['hometown'], dict_['sex'], dict_['age'])
                        print(dict_)
                    else:
                        if len(dict_) != 0:
                            if 'sex' not in dict_ and 'hometown' in dict_ and 'age' in dict_:
                                VkBot.send_msg(user_id, f'Не все параметры заданы \n'
                                                        f'Пол: - \n'
                                                        f'Возраст: {dict_["age"]} \n'
                                                        f'Город: {dict_["hometown"]}', self.set_search_keyboard())

                            elif 'hometown' not in dict_ and 'sex' in dict_ and 'age' in dict_:
                                if dict_['sex'] == 1:
                                    sex_ = 'женщины'
                                else:
                                    sex_ = 'мужчины'
                                VkBot.send_msg(user_id, f'Не все параметры заданы \n'
                                                        f'Пол: {sex_} \n'
                                                        f'Возраст: {dict_["age"]} \n'
                                                        f'Город: -', self.set_search_keyboard())

                            elif 'age' not in dict_ and 'hometown' in dict_ and 'sex' in dict_:
                                if dict_['sex'] == 1:
                                    sex_ = 'женщины'
                                else:
                                    sex_ = 'мужчины'
                                VkBot.send_msg(user_id, f'Не все параметры заданы \n'
                                                        f'Пол: {sex_} \n'
                                                        f'Возраст: -\n'
                                                        f'Город: {dict_["hometown"]}', self.set_search_keyboard())

                            elif 'age' not in dict_ and 'hometown' not in dict_:
                                if dict_['sex'] == 1:
                                    sex_ = 'женщины'
                                else:
                                    sex_ = 'мужчины'
                                VkBot.send_msg(user_id, f'Не все параметры заданы \n'
                                                        f'Пол: {sex_} \n'
                                                        f'Возраст: -\n'
                                                        f'Город: -', self.set_search_keyboard())

                            elif 'age' not in dict_ and 'sex' not in dict_:
                                VkBot.send_msg(user_id, f'Не все параметры заданы \n'
                                                        f'Пол: -\n'
                                                        f'Возраст: -\n'
                                                        f'Город: {dict_["hometown"]}', self.set_search_keyboard())

                            elif 'hometown' not in dict_ and 'sex' not in dict_:
                                VkBot.send_msg(user_id, f'Не все параметры заданы \n'
                                                        f'Пол: -\n'
                                                        f'Возраст: {dict_["age"]} \n'
                                                        f'Город: -', self.set_search_keyboard())

                        else:
                            VkBot.send_msg(user_id, f'Не все параметры заданы \n'
                                                    f'Пол: -\n'
                                                    f'Возраст: -\n'
                                                    f'Город: -', self.set_search_keyboard())



                elif text == 'возраст':
                    VkBot.send_msg(user_id, 'Введите возраст от 14 до 100', self.set_search_keyboard())
                    dict_['age'] = self.get_age(user_id)
                    print(dict_)


    def see_fav(self, user_id):
        list_users = list_favorite()

        y = 0
        if len(list_users) != 0:
            i = list_users[y]
            photo_ = get_photo(i.get('vk_id'))
            VkBot.send_msg(user_id, f"""{i.get('name')} {i.get('surname')}\n{i.get('link')}""")
            photo = "photo{}_{}".format(photo_['owner_id'],
                                        photo_['photo_id'])
            vk_session.method("messages.send", {'peer_id': user_id, 'attachment': photo,
                                                "random_id": randrange(10**5)})

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    text = event.text.lower()
                    user_vk_id = event.user_id

                    if text == 'удалить':
                        delete_db_elit(i.get('vk_id'))
                        VkBot.send_msg(user_id, f"""Вы удалили {i.get('name')} {i.get('surname')}""")
                        y += 1
                        if y <= len(list_users) - 1:
                            i = list_users[y]
                            photo_ = get_photo(i.get('vk_id'))
                            VkBot.send_msg(user_id, f"""{i.get('name')} {i.get('surname')}\n{i.get('link')}""")
                            photo = "photo{}_{}".format(photo_['owner_id'],
                                                        photo_['photo_id'])
                            vk_session.method("messages.send", {'peer_id': user_id, 'attachment': photo,
                                                                "random_id": randrange(10 ** 5)})
                        else:
                            VkBot.send_msg(user_id, f'это все!', self.set_keyboard_start())
                            self.starting()

                    elif text == 'следующее':
                        y += 1
                        if y <= len(list_users) - 1:
                            i = list_users[y]
                            photo_ = get_photo(i.get('vk_id'))
                            VkBot.send_msg(user_id, f"""{i.get('name')} {i.get('surname')}\n{i.get('link')}""")
                            photo = "photo{}_{}".format(photo_['owner_id'],
                                                        photo_['photo_id'])
                            vk_session.method("messages.send", {'peer_id': user_id, 'attachment': photo,
                                                                "random_id": randrange(10**5)})
                        else:
                            VkBot.send_msg(user_id, f'это все!', self.set_keyboard_start())
                            self.starting()

                    elif text == 'назад':
                        VkBot.send_msg(user_id, 'Начнём сначала', self.set_keyboard_start())
                        self.starting()

                    else:
                        VkBot.send_msg(user_id, 'Не понимаю о чём вы..', self.set_keyboard_start())
                        self.starting()
        else:
            VkBot.send_msg(user_id, f'это все!', self.set_keyboard_start())
            self.starting()


    ##!!! ОСНОВНАЯ ФУНКЦИЯ
    def starting(self):
        dict_new_ = {}
        for event in longpoll.listen():

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text.lower()
                user_id = event.user_id

                if check_db_reg(user_id) is None:
                    register_user(user_id)
                    if text in MsgBot.greetings:
                        VkBot.send_msg(user_id, MsgBot.start, self.set_keyboard_start())

                    elif text == 'задать критерии':
                        VkBot.send_msg(user_id, 'Тогда давай введём параметры для вашей второй половинки', self.set_search_keyboard())
                        dict_new_ = self.set_search_params(user_id)


                    elif text == 'назад' or text == 'Назад':
                        VkBot.send_msg(user_id, 'Начнём сначала', self.set_keyboard_start())
                        self.starting()

                    elif text == 'посмотреть избранное':
                        VkBot.send_msg(user_id, 'Сохраненные:', self.elit_keyboard())
                        self.see_fav(user_id)

                    elif text == MsgBot.leav:
                        VkBot.send_msg(user_id, MsgBot.gd, self.set_keyboard_start())

                    else:
                        VkBot.send_msg(user_id, MsgBot.misunderstand, self.set_keyboard_start())

                else:
                    if text in MsgBot.greetings:
                        VkBot.send_msg(user_id, MsgBot.start, self.set_keyboard_start())

                    elif text == 'задать критерии':
                        VkBot.send_msg(user_id, 'Тогда давай введём параметры для вашей второй половинки',
                                       self.set_search_keyboard())
                        dict_new_ = self.set_search_params(user_id)

                    elif text == 'назад' or text == 'Назад':
                        VkBot.send_msg(user_id, 'Начнём сначала', self.set_keyboard_start())
                        self.starting()

                    elif text == 'посмотреть избранное':
                        VkBot.send_msg(user_id, 'Сохраненные:', self.elit_keyboard())
                        self.see_fav(user_id)

                    elif text == MsgBot.leav:
                        VkBot.send_msg(user_id, MsgBot.gd, self.set_keyboard_start())

                    else:
                        VkBot.send_msg(user_id, MsgBot.misunderstand, self.set_keyboard_start())

bot = VkBot()
bot.starting()



