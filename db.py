import json
import logging
from datetime import datetime

import uuid
from sqlalchemy import create_engine, exists, BigInteger, delete, LargeBinary, DateTime, text, JSON

from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base



engine = create_engine('postgresql://postgres:123456@localhost:5432/postgres')
Base = declarative_base()


with engine.connect() as conn:
    conn.execute(text("create schema if not exists links;"))

class Reflink(Base):
    __tablename__ = 'links'
    __table_args__ = {'schema': 'links'}
    user_id = Column(Integer, primary_key=True)
    links = Column(JSON, default={})
    datetime = Column(DateTime)



Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

session.commit()



def save_link(user_id, link):
    time = datetime.now()
    link_id = str(uuid.uuid4())

    try:
        link_data = session.query(Reflink).filter_by(user_id=user_id).first()
        if link_data:
            link_data.links = json.loads(link_data.links) if isinstance(link_data.links, str) else link_data.links
            link_data.links[link_id] = f"{link}-{time.strftime('%H:%M:%S_%d/%m/%Y')}"
            logging.info("Link updated successfully.")
        else:
            link_data = Reflink(user_id=user_id, links={link_id: link}, datetime=time)
            logging.info("New record created successfully.")

        session.add(link_data)
        session.commit()
        return link_id

    except SQLAlchemyError as e:
        logging.error("An error occurred while saving the link: {}".format(str(e)))
        session.rollback()
        raise

def get_link(link_id):
    return session.query(Reflink).filter(Reflink.links.has_key(link_id)).first()



#save_link('1212131', 'http://link.com')


print(*[[i.user_id, i.links, i.datetime] for i in session.query(Reflink).all()], sep='\n')

#print(*[[i.id, i.filetype, i.option, i.user_id, i.user_name, i.datetime] for i in session.query(File).all()], sep='\n')





def del_table(table):
    session.query(Reflink).delete()
    session.commit()




# del_table('files')
#g = [[i.datetime, i.filename] for i in session.query(File).all()]
#print(len(g), *g, sep='\n')












# def items(item: str):
#     g = {
#         'planets': [(i.planet_name, i.planet_name) for i in session.query(Planets).all()],
#         'passengers': [(i.passenger_name, i.passenger_name) for i in session.query(Passengers).all()],
#         'ships': [(i.ship_name, i.ship_name) for i in session.query(Ships).all()]
#
#     }
#     return g[item]
#
#
#
#
# def table_info(tablename: str, item = None):
#     pl = session.query(Planets).filter(Planets.planet_name == item).all()
#     ps = session.query(Passengers).filter(Passengers.passenger_name == item).all()
#     sh = session.query(Ships).filter(Ships.ship_name == item).all()
#
#     tables = {
#         'planets': {
#             False: '\n'.join([f"Space object: {i.planet_name}\nType: {i.planet_class}\nMain parameters: {i.parameters}\nAge (th.years): {i.age}"
#                              for i in session.query(Planets).all()]),
#             True: f"Planet name: {pl[0].planet_name}\nType: {pl[0].planet_class}\nMain parameters: {pl[0].parameters}\nAge (th.years): {pl[0].age}"
#             if session.query(exists().where(Planets.planet_name == item)).scalar() else 'No such planet in our database'
#             },
#         'passengers': {
#             False: '\n'.join([f"Passenger name: {i.passenger_name}\nMain data: {i.parameters}\nAge (years): {i.age}"
#                              for i in session.query(Passengers).all()]),
#             True: f"Passenger name: {ps[0].passenger_name}\nMain data: {ps[0].parameters}\nAge (years): {ps[0].age}"
#             if session.query(exists().where(Passengers.passenger_name == item)).scalar() else 'No such passenger in our database'
#         },
#         'ships': {
#             False: '\n'.join(
#                 [f"Ship name: {i.ship_name}\nShip class: {i.ship_class}\nMain parameter: {i.parameters}"
#                  for i in session.query(Ships).all()]),
#             True: f"Ship name: {sh[0].ship_name}\nShip class: {sh[0].ship_class}\nMain parameter: {sh[0].parameters}"
#             if session.query(
#                 exists().where(Ships.ship_name == item)).scalar() else 'No such ship in our database'
#         }
#         }
#     return tables[tablename][bool(item)]
#
#
#
# def del_table(table):
#     session.query(Planets).delete()
#     session.commit()
#
#
# def del_item(kind, item):
#     g = {
#         'planets': session.query(Planets).where(Planets.planet_name == item).delete(),
#         'passengers': session.query(Passengers).where(Passengers.passenger_name == item).delete(),
#         'ships': session.query(Ships).where(Ships.ship_name == item).delete(),
#     }
#     g[kind]
#     session.commit()
#
#
#
# def add_new_object(tablename, *args):
#     g = list(args)
#     if len(args) < 4:
#         g.append(None)
#     tables = {
#         'planets': Planets(
#             planet_name=g[0],
#             planet_class=g[1],
#             parameters=g[2],
#             age=g[3]
#         ),
#         'passengers': Passengers(
#             passenger_name=g[0],
#             parameters=g[1],
#             age=g[2]
#         ),
#         'ships': Ships(
#             ship_name=g[0],
#             ship_class=g[1],
#             parameters=g[2]
#         )
#     }
#     session.add(tables[tablename])
#     session.commit()



#add_new_object('planets', 'Tatooine', 'desert planet', "Homeland of person who had to fight evil Not to join it! And his kidness son.", 8)

#add_new_object('passengers', 'Luke Skywalker', 'experience - New Hope of Jedi kind - 83kg, height - 183cm, sex - man', 25)
#
#add_new_object('ships', 'Millennium Falcon', 'YT-series', "weight - 30 t. tons, length - 34 m, width - 25 m, height - 8 m")

#print(table_info('planets'))
#del_item('passengers', 'ps_Serg.Ripley')

# print(items('ships'))












