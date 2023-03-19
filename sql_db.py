import sqlalchemy
import vk_api

from sqlalchemy import create_engine, Integer, Table, Column, String, ForeignKey
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from vk_api.longpoll import VkLongPoll, VkEventType
group_token = 'vk1.a.j3dPowsPmxhGrUbQbGvR4akT90Actz4SGW80FkVAqCGMHxGtAIdGU2kp49wBF7Zzf_V7eszpOsnPjbNHPd3-j3DyDXSnD1lnPijGnKDaQM4osi26BoTt6WnfDgFjNZzOwx5plkhclTqdJduTfNgIAFtSCdsW2IK6vVCSGFYWBKyzH342_DRZjBfLbnl3zLN3ykTEGGMtwJWGFNma1Cgm2Q'
vk = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(vk)

engine = create_engine("postgresql+psycopg2://mista:Mike200789@localhost/vvvkinder")
con = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_vk = Column(Integer, unique=True)

class Half(Base):
    __tablename__ = 'half'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = (Integer, ForeignKey('user.id', ondelete='CASCADE'))
    link = Column(String)
    vk_id = Column(Integer)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    gender = Column(Integer)
    city = Column(String)
    photo = Column(String)




Base.metadata.create_all(engine)


#1 Регистрация пользователя
def register_user(vk_id):

    try:
        new_user = User(id_vk=vk_id)
        session.add(new_user)
        session.commit()
        return True

    except (IntegrityError, InvalidRequestError):
        return False

#2 Проверка регистрации пользователя бота в БД
def check_db_reg(ids):

    current_user_id = session.query(User).filter_by(id_vk=ids).first()
    return current_user_id

#3 Проверка Userа в БД
def check_db_user(ids):

    second_half_user = session.query(Half).filter_by(vk_id=ids).first()
    return second_half_user



#5 Удаляет Userа из избранного
def delete_db_elit(ids):

    current_user = session.query(Half).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()

#6 Сохраняем нужного пользователя в БД
def add_user(vk_id, name, surname, gender, year, city, link, photo, id_user):

    try:
        new_user = Half(
            vk_id=vk_id,
            name=name,
            surname=surname,
            gender=gender,
            age=year,
            city=city,
            link=link,
            photo=photo,
            user_id=id_user
        )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False

#6 Список избранное
def list_favorite():

    list_users = []
    users = session.query(Half).all()

    for user in users:
        pers = {'id': user.id, 'vk_id': user.vk_id, 'name': user.name, 'surname': user.surname, 'link': user.link, 'photo': user.photo}
        list_users.append(pers)
    return list_users



# register_user(9742231)
# print(check_db_reg(9742231))

