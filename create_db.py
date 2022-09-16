from database import Base, engine
from models import User

print('Creating Database....')

Base.metadata.create_all(engine)