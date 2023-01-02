import requests

gare = "Europe"

from datetime import datetime

#-----------------------base sql alchemy---------------------------
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime

engine = create_engine('sqlite:///objtouvee.sqlite')
Base = declarative_base()

class ObjetTrouve(Base):
    __tablename__ = "ObjetTrouve"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gare = Column(String)
    date = Column(DateTime)
    type = Column(String)
    nature = Column(String)

Base.metadata.create_all(engine)

#table crées : 
print(engine.table_names())

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

#--------------------------api_request--------
for annee in range(2016,2023):
    print(annee)
    url = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&rows=10000&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.gc_obo_gare_origine_r_name=Lille+{gare}&refine.date={annee}"
    response = requests.get(url)
    reponse_json = response.json()


    print("add obj")
    for row in reponse_json["records"]:
        obj = ObjetTrouve(gare=row["fields"]["gc_obo_gare_origine_r_name"],
            date=datetime.fromisoformat(row["fields"]["date"]),
            type=row["fields"]["gc_obo_type_c"],
            nature = row["fields"]["gc_obo_nature_c"])
        session.add(obj)
session.commit()