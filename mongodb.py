from pymongo import MongoClient
import os
client = MongoClient("mongodb+srv://trinhsk:Bon78952%40@ncifrederick-l7ves.mongodb.net/test?retryWrites=true")
client = MongoClient("mongodb+srv://sktrinh12:Bon78952%40@ncifrederick-l7ves.mongodb.net/test?retryWrites=true")

db = client.ncifred

filepath = 'Users/trinhsk/Documents/absVizFlask/NCIFrederick/textfiles/'
filepath = '/Users/spencertrinh/GitRepos/absViz/NCIFrederick/textfiles/'

def insertMongoDb(pltcode,db,filepath):
    collection = db[pltcode]
    columns = []
    count=0
    with open(filepath,mode='r',encoding='utf-16') as f:
        for row in f:
            row = row.strip().split('\t')
            if row[0] == '':  
                break
            if count< 2:
                pass
            elif count == 2:
                columns.append(row)
            else:
                datadict = {columns[0][i] : float(row[i]) for i in range(len(row))}
                result = collection.insert_one(datadict)
                print(f'Inserted {result.inserted_id}, ({count})')
            count +=1

def checkDirAddMongoDb(db,filepath):
    for f in os.listdir(filepath):
        if f.replace('.txt','') in db.list_collection_names():
            pass
        else:
            os.path.isfile(os.path.join(filepath,f))
            fp = os.path.join(filepath,f)
            pltcode = f.replace('.txt','')
            insertMongoDb(pltcode,db,fp)
            print(fp)

collection  = db[pltcode]
collection.remove()
collection.drop()
client.close()

def getWavelengthData(db,pltcode_suffix,wavelength):
    res=db[pltcode_suffix].find({"Wavelength":wavelength})
    return {k:v for k,v in res[0].items() if k not in ['_id','Wavelength','Temperature(¡C)']}
    
for i in db['14190301100'].find({}, {'A1':1,'_id':0}):
    print(i)
getWavelengthData(db,'14190301100',390).keys()



