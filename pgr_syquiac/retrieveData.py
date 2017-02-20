'''
Pauline Ramirez & Carlos Syquia

'''


import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import sodapy

class retrieveData(dml.Algorithm):
    contributor = 'pgr_syquiac'
    reads = []
    writes = ['pgr_syquiac.hospitals', 'pgr_syquiac.cdc', 'pgr_syquiac.schools','pgr_syquiac.pools','pgr_syquiac.stores']
    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('pgr_syquiac', 'pgr_syquiac')

        # Get data for hospitals
        client = sodapy.Socrata("data.cityofboston.gov", None)
        response = client.get("u6fv-m8v4", limit=30)
        repo.dropCollection("hospitals")
        repo.createCollection("hospitals")
        repo['pgr_syquiac.hospitals'].insert_many(response)

        # Get data for CDC 500 cities
        client = sodapy.Socrata("chronicdata.cdc.gov", None)
        response = client.get("csmm-fdhi", CityName="Boston",
        GeographicLevel="Census Tract", limit=5000)
        #print(len(response))
        repo.dropCollection("cdc")
        repo.createCollection("cdc")
        repo['pgr_syquiac.cdc'].insert_many(response)

        # Get data for all universities in the US
        url = 'http://datamechanics.io/data/pgr_syquiac/universities.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("schools")
        repo.createCollection("schools")
        repo['pgr_syquiac.schools'].insert_many(r)


        # Get data for Open Swimming Pools in Boston
        client = sodapy.Socrata("data.cityofboston.gov", None)
        response = client.get("5jxx-wfpr", limit=1)
        #print(response)
        repo.dropCollection("pools")
        repo.createCollection("pools")
        repo['pgr_syquiac.pools'].insert_many(response)

        # Get data for healthy corner stores
        client = sodapy.Socrata("data.cityofboston.gov", None)
        response = client.get("ybm6-m5qd", limit=16)
        #print(response)
        repo.dropCollection("stores")
        repo.createCollection("stores")
        repo['pgr_syquiac.stores'].insert_many(response)


        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}

    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('pgr_syquiac', 'pgr_syquiac')


        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/') #Boston Data Portal
        doc.add_namespace('cdc', 'https://chronicdata.cdc.gov/resource/') #CDC data portal
        doc.add_namespace('cdp', 'https://data.cambridgema.gov/resource/')
        doc.add_namespace('datm', 'https://datamechanics.io/data') # datamechanics.io, hosts the university data

        this_script = doc.agent('alg:pgr_syquiac#retrieveData', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})

        #hospitals
        hospitalsResource = doc.entity('bdp:u6fv-m8v4', {'prov:label':'Hospital Locations', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        getHospitals = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(getHospitals, this_script)
        doc.usage(getHospitals, hospitalsResource, startTime)#, None)

        #cdc Data
        cdcResource = doc.entity('cdc:csmm-fdhi', {'prov:label':'500 Cities: Local Data for Better Health', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        getCDC = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(getCDC, this_script)
        doc.usage(getCDC, cdcResource, startTime)#, None)

        #university data
        schoolsResource = doc.entity('datm:pgr_syquia/universities', {'prov:label':'Schools', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        getSchools = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(getSchools, this_script)
        doc.usage(getSchools, schoolsResource, startTime)#, None)

        #Open Swimming Pools data
        poolsResource = doc.entity('bdp:5jxx-wfpr', {'prov:label':'Pools', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        getPools = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(getPools, this_script)
        doc.usage(getPools, poolsResource, startTime)#, None)

        #healthy corner stores data
        storesResource = doc.entity('bdp:ybm6-m5qd', {'prov:label':'Healthy Corner Stores', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        getStores = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(getStores, this_script)
        doc.usage(getStores, storesResource, startTime)#, None)

        '''
        # This is for when u create new data

        lost = doc.entity('dat:alice_bob#lost', {prov.model.PROV_LABEL:'Animals Lost', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(lost, this_script)
        doc.wasGeneratedBy(lost, get_lost, endTime)
        doc.wasDerivedFrom(lost, resource, get_lost, get_lost, get_lost)

        found = doc.entity('dat:alice_bob#found', {prov.model.PROV_LABEL:'Animals Found', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(found, this_script)
        doc.wasGeneratedBy(found, get_found, endTime)
        doc.wasDerivedFrom(found, resource, get_found, get_found, get_found)

        '''
        #repo.record(doc.serialize()) # Record the provenance document. <- creates an error
        repo.logout()

        return doc

retrieveData.execute()
doc = retrieveData.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
