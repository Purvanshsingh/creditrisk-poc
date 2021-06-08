from API_Doc.creditrisk_api_doc import doc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.app_factory import app_factory
from hydrus.utils import set_session, set_doc, set_hydrus_server_url, set_api_name
from hydra_python_core import doc_maker
from hydrus.data import doc_parse
from hydrus.data.db_models import Base, create_database_tables

HYDRUS_SERVER_URL = "http://localhost:8080/"
API_NAME = "creditrisk_api"

apidoc = doc_maker.create_doc(doc, HYDRUS_SERVER_URL, API_NAME)

engine = create_engine('sqlite:///database.db')
classes = doc_parse.get_classes(apidoc)
# Drop all existing models and add the new ones.
Base.metadata.drop_all(engine)
# creating the DB tables
create_database_tables(classes)
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()

if __name__ == "__main__":
    app = app_factory(API_NAME)
    # Set the name of the API
    with set_api_name(app, API_NAME):
       # Set the API Documentation
       with set_doc(app, apidoc):
           # Set HYDRUS_SERVER_URL
           with set_hydrus_server_url(app, HYDRUS_SERVER_URL):
               # Set the Database session
               with set_session(app, session):
                   # Start the hydrus app
                   app.run(host='127.0.0.1', debug=True, port=8080)