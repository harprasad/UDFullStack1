from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Categories(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }

class SportsItem(Base):
    __tablename__  = "sportsitem"
    id = Column(Integer,primary_key = True)
    name = Column(String(250),nullable = False)
    info = Column(String(1000),nullable = True)
    CategoryId = Column(Integer,ForeignKey(Categories.id))
    category = relationship(Categories)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'info': self.info,
            'id': self.id,
        }

engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.create_all(engine)