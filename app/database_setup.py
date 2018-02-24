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
           'items'        : [],
       }


class User(Base):
    __tablename__  = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class SportsItem(Base):
    __tablename__  = "sportsitem"

    id = Column(Integer,primary_key = True)
    name = Column(String(250),nullable = False)
    info = Column(String(1000),nullable = True)
    CategoryId = Column(Integer,ForeignKey(Categories.id))
    category = relationship(Categories)
    userId = Column(Integer,ForeignKey(User.id))
    user = relationship(User)
    
    @property
    def serialize(self):
        return {
            'name': self.name,
            'info': self.info,
            'id': self.id,
            'categoryID':self.CategoryId,
            'categoryName':self.category.name
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)