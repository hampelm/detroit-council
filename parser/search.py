import solr 
from pymongo import Connection
from xml.sax.saxutils import escape

illegal = ["\x00","\x01","\x02","\x03","\x04","\x05","\x06","\x07","\x08","\x0B"," \x0C","\x0E","\x0F","\x10","\x11","\x12","\x13","\x14","\x15","\x16","\x17","\x18","\x19","\x1A"," \x1B","\x1C","\x1D","\x1E","\x1F"]

# Save the stuff to Mongo
connection = Connection('localhost', 27017)
db = connection.council
collection = db.blocks    
    
# Save the stuff to solr

s = solr.SolrConnection('http://localhost:8983/solr')
s.delete(queries=['*:*'])


batch = []
everything = collection.find()
for elt in everything:
    doc = {'id': str(elt['_id']), 'features': elt['string'] }
    
    for char in illegal:
        doc['features'] = doc['features'].replace(char,'')
    
    batch.append(doc)
    
s.add_many(batch,_commit=True)


