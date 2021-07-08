from connection import Db
from models import Consumable

class Repository:

    @staticmethod
    def create(consumable):
        session = Db.startSession()
        session.add(consumable)
        session.commit()
        Db.closeSession(session)
        
    @staticmethod
    def createAll(consumables):
        session = Db.startSession()
        for consumable in consumables:
            session.add(consumable)
        session.commit()
        Db.closeSession(session)

    @staticmethod
    def readAllUndeleted(art_type):
        session = Db.startSession()
        results = session.query(Consumable.id, Consumable.art_type, Consumable.name, \
                        Consumable.start_date, Consumable.end_date, Consumable.consum_time_hrs, \
                        Consumable.rating, Consumable.consum_days) \
                    .filter(Consumable.art_type==art_type,Consumable.deleted=='False').order_by(Consumable.id).all()
        Db.closeSession(session)
        return results

    @staticmethod
    def readById(id):
        session = Db.startSession()
        result = session.query(Consumable).get(id)
        Db.closeSession(session)
        return result

    @staticmethod
    def deleteById(id):
        session = Db.startSession()
        # session.query(Consumable).filter(Consumable.id == id).delete()
        session.query(Consumable).filter(Consumable.id==id).\
            update({'deleted':True}
            ,synchronize_session=False)
        session.commit()
        Db.closeSession(session)

    @staticmethod
    def update(consumable):
        session = Db.startSession()
        session.query(Consumable).filter(Consumable.id==consumable.id).\
            update({'consum_time_hrs':consumable.consum_time_hrs, 
                    'consum_days':consumable.consum_days,
                    'rating':consumable.rating,
                    'end_date':consumable.end_date}
            ,synchronize_session=False)
        session.commit()
        Db.closeSession(session)

    @staticmethod
    def readAll():
        session = Db.startSession()
        results = session.query(Consumable.id, Consumable.art_type, Consumable.name, \
                        Consumable.start_date, Consumable.end_date, Consumable.consum_time_hrs, \
                        Consumable.rating, Consumable.consum_days) \
                    .order_by(Consumable.id).all()
        Db.closeSession(session)
        return results


