# optimizeBusRoute.py

# import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import math
import random
from heapq import heappush, heappop
from geopy.distance import vincenty

class optimizeBusRoute(dml.Algorithm):
    contributor = 'echogu_wei0496_wuhaoyu'
    reads = ['echogu_wei0496_wuhaoyu.assigned_students']
    writes = ['echogu_wei0496_wuhaoyu.bus_route']

    @staticmethod
    def execute(trial = False):
        ''' optimize school bus route
        '''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('echogu_wei0496_wuhaoyu', 'echogu_wei0496_wuhaoyu')

        # Trial mode
        if trial:
            pass

        # loads the collection
        raw_assigned_students = repo['echogu_wei0496_wuhaoyu.assigned_students'].find()
        assigned_students = []
        for item in raw_assigned_students:
            assigned_students.append({'aggregated_points': item['aggregated_points'], 'points': item['points']})

        # utilize minimum spanning tree to find bus route
        result = optimizeBusRoute.find_mst(assigned_students)

        repo.dropCollection('bus_route')
        repo.createCollection('bus_route')
        for i in result:
            repo['echogu_wei0496_wuhaoyu.bus_route'].insert_one(i)
        repo['echogu_wei0496_wuhaoyu.bus_route'].metadata({'complete': True})
        print(repo['echogu_wei0496_wuhaoyu.bus_route'].metadata(), "Saved Bus Route")

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}

    @staticmethod
    def provenance(doc=prov.model.ProvDocument(), startTime=None, endTime=None):
        ''' Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
        '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('echogu_wei0496_wuhaoyu', 'echogu_wei0496_wuhaoyu')

        # create document object and define namespaces
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/')  # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/')  # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#')  # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/')  # The event log.

        # define entity to represent resources
        this_script = doc.agent('alg:echogu_wei0496_wuhaoyu#optimizeBusRoute', {prov.model.PROV_TYPE: prov.model.PROV['SoftwareAgent'], 'ont:Extension': 'py'})
        assigned_students = doc.entity('dat:echogu_wei0496_wuhaoyu#assigned_students', {'prov:label': 'assigned_students', prov.model.PROV_TYPE: 'ont:DataSet'})

        # define activity to represent invocaton of the script
        run_optimizeBusRoute = doc.activity('log:uuid' + str(uuid.uuid4()), startTime, endTime)
        # associate the activity with the script
        doc.wasAssociatedWith(run_optimizeBusRoute, this_script)
        # indicate that an activity used the entity
        doc.usage(run_optimizeBusRoute, assigned_students, startTime, None, {prov.model.PROV_TYPE: 'ont:Computation'})

        # for the data obtained, indicate that the entity was attributed to what agent, was generated by which activity and was derived from what entity
        bus_route = doc.entity('dat:echogu_wei0496_wuhaoyu#optimizeBusRoute', {prov.model.PROV_LABEL: 'bus_route', prov.model.PROV_TYPE: 'ont:DataSet'})
        doc.wasAttributedTo(bus_route, this_script)
        doc.wasGeneratedBy(bus_route, run_optimizeBusRoute, endTime)
        doc.wasDerivedFrom(bus_route, assigned_students, run_optimizeBusRoute, run_optimizeBusRoute, run_optimizeBusRoute)

        repo.logout()

        return doc

    # This is the helper function to find MST among all student pick up points
    # input: [coordinates] restricted by n(bus capacity, this is the maximum size of the tree)
    # convert the original input into format
    @staticmethod
    def find_mst(assigned_students):
        final_res = []
        for i in assigned_students:
            points = i['points']
            K_points = i['aggregated_points'][0]
            final = []
            results = []
            for j in points:
                results.append([j["latitude"], j["longitude"], j['student_id']])
            #print("printing results")
            #print(results)
            res = optimizeBusRoute.cal_MST(results)
            print(res)
            for k in res[0]:
                final.append({
                        'student_id': results[k][2],
                        'latitude': results[k][0],
                        'longitude': results[k][1]})

            final_res.append({
                'aggregated_points':K_points,
                'Pickup_sequence': final})
        return final_res

    @staticmethod
    def cal_MST(points):
        if(len(points) != 1):
            # construct a adjacency matrix
            adjacency_matrix = optimizeBusRoute.generate_graph(points)
            result = optimizeBusRoute.Prim(adjacency_matrix)

            return result

        # When points contains only one student, no need to run MST
        else:
            return [0], 0

    # Initialization the adjacency matrix for the tree
    @staticmethod
    def generate_graph(points):
        # initialize the adjacency matrix
        adjacency_matrix = [[100 for x in range(len(points))] for y in range(len(points))]
        for i in range(len(points)-1):
            for j in range(i+1, len(points)):
                adjacency_matrix[i][j] = optimizeBusRoute.distance(points[i][0:2], points[j][0:2])
                adjacency_matrix[j][i] = adjacency_matrix[i][j]
        return adjacency_matrix

    # Run MST Prim's Algorithm
    # Takes the random graph G as input and return the route and
    # the total weight of the MST
    @staticmethod
    def Prim(G):
        # print(G)
        # Initialize the final weight to 0
        result = 0
        # Initialize keys of all vertices as infinite
        adjacency_matrix = [[2] * len(G)] * len(G)
        # Initialize an empty priority queue
        heap = []
        # Initialize an empty set of explored nodes S
        S = []
        # Insert source vertex into priority queue with key 0
        heappush(heap, [0, 1])
        # Initialize an empty array which each index equals 1 if the node has been explored and 0 if not
        Lookup = [0] * len(G)
        # Insert remaining vertex into priority queue with infinity key
        for i in range(1, len(G)):
            heappush(heap, [2, i])

        while sum(Lookup) != len(G):
            u = heappop(heap)

            # ignore all subsequent duplicates
            if Lookup[u[1]] == 0:
            # if u[1] not in S:
                S += [u[1]]
                Lookup[u[1]] = 1
                result += u[0]
                # for each edge e = (u,v)
                for v in range(len(G)):
                    # since in assumption it is a complete graph, we do not have to check if an edge exists
                    #if v not in S:
                    if Lookup[v] == 0:
                        # Since it's not efficient to lookup and modify existing tuples in the heap
                        # We can just insert the new tuple, upon removal we still have the lowest edge
                        heappush(heap, [G[u[1]][v], v])
        return S, result

    @staticmethod
    def distance(point1, point2):
        return vincenty(point1, point2).miles

# optimizeBusRoute.execute()
# doc = optimizeBusRoute.provenance()
# print(doc.get_provn())
# print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
