import database_setup
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker(bind = database_setup.engine)
session = DBSession()

soccer = database_setup.Categories(name = "Soccer")
basketball = database_setup.Categories(name = "BasketBall")
hockey = database_setup.Categories(name = "Hockey")
skating = database_setup.Categories(name = "Skating")
rockclimbing = database_setup.Categories(name = "Rockclimbing")
frisbee = database_setup.Categories(name = "Frisbee")
foosball = database_setup.Categories(name = "Foosball")

session.add(soccer)
session.add(basketball)
session.add(hockey)
session.add(skating)
session.add(rockclimbing)
session.add(frisbee)
session.add(foosball)
session.commit()

for category in session.query(database_setup.Categories):
    print category.name

