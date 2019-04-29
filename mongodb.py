from pymongo import MongoClient
import os
client = MongoClient("mongodb+srv://trinhsk:Bon78952%40@ncifrederick-l7ves.mongodb.net/test?retryWrites=true")

db = client.ncifred


filepath = '/Users/trinhsk/Documents/absVizFlask/NCIFrederick/textfiles/'

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

for f in os.listdir(filepath): 
    if f in db.collection_names():
        pass
    else: os.path.isfile(os.path.join(filepath,f)) :
        fp = os.path.join(filepath,f) 
        pltcode = f.replace('.txt','')
        insertMongoDb(pltcode,db,fp)


collection  = db[pltcode]
collection.remove()
collection.drop()
client.close()

res=db['14190301200'].find({"Wavelength":230})
res[0]
for i in res:
    print(i)


