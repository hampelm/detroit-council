from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response

from pymongo import Connection, objectid, ASCENDING
from calais import Calais
import datetime 

def connection():
    conn = Connection('localhost', 27017)
    db = conn.council
    blocks = db.blocks
    return blocks
    


# Create your views here.
def home(request):
    collection = connection()
    blocks = collection.distinct('date')
    for block in blocks:
        print block
    return render_to_response('home.html', {'blocks':blocks})


def member(request, member):
    collection = connection()
    blocks = collection.find( {'$or': [ {'yeas':member}, {'nays':member}], 'type':'contract'}, sort=[('date', ASCENDING)] )
    
    return render_to_response('member.html', {'blocks': blocks, 'member':member})
    
def meeting(request, y, m, d):
    date = datetime.datetime(int(y),int(m),int(d))
    collection = connection()
    blocks = collection.find( {'date': date} )


    return render_to_response('meeting.html', {'blocks': blocks, 'date':date})
    
def item(request, y, m, d, item):
    collection = connection()
    block = collection.find_one( {'_id': objectid.ObjectId(item)})
    print block
    return render_to_response('item.html', {'item':block })
    
    
def contract(request, contract):

    collection = connection()
    blocks = collection.find( { 'contracts':contract}, sort=[('date', ASCENDING)] )
   # 
   # calais = Calais(settings.CALAIS, submitter="hello world")
   # 
   # newbloks = []
   # for block in blocks:
   #     block['entities'] = calais.analyze(block['string']).entities
   #     newbloks.append(block)
    
    return render_to_response('item.html', {'blocks': blocks})
