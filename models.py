from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.operators import endswith_op
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence
from sqlalchemy.sql.sqltypes import Boolean, Date, DateTime, Integer, Numeric, String, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from connection import engine

Base = declarative_base()

#### !! A 'Consumable' refers to an art_item..
#### ..e.g. 'Book', 'Movie' each of them is a 'Consumable'

### Consumable model
class Consumable(Base):
    __tablename__ = 'consumables'
    id = Column(Integer, Sequence('consumable_id_seq'), primary_key=True)
    art_type = Column(String(20), nullable=False)
    name = Column(String(80), nullable=False)
    start_date = Column(Date(), nullable=True)
    end_date = Column(Date(), nullable=True)
    consum_time_hrs = Column(Integer, default=0)
    rating = Column(Numeric(10,2), nullable=True)
    consum_days = Column(Integer, default=0)
    deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "<Consumable(id='%d', art_type='%s' name='%s', start_date='%s', end_date='%s',\
                consum_time_hrs='%s', rating='%s', consum_days='%s', deleted='%s'\
                created_at='%s', updated_at='%s')>" % ( 
            self.id, self.art_type, self.name, self.start_date, self.end_date,  
            self.consum_time_hrs, self.rating, self.consum_days, self.deleted,
            self.created_at, self.updated_at)


# --- Creating the tables --- 
Base.metadata.create_all(bind=engine) 
