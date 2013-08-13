from sqlalchemy import *
engine = create_engine('sqlite:///iatidata_new.sqlite', echo=False)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
Session = sessionmaker()
session = Session()

models = declarative_base()
models.metadata.bind = engine

models.metadata.create_all()
