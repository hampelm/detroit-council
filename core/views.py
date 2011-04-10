from django import forms
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response

from calais import Calais
import datetime 
from pymongo import Connection, objectid, ASCENDING
import solr 


#======= Helpers
class SearchForm(forms.Form):
    q = forms.CharField(max_length=100)


def connection():
    conn = Connection('localhost', 27017)
    db = conn.council
    blocks = db.blocks
    return blocks    
    
def member_slugs_mapping():
    conn = Connection('localhost', 27017)
    db = conn.council
    memberdb = db.members
    mappings = memberdb.find()
    return mappings[0]


#======= Views
def test(request):
    response = {}
    collection = connection()
    
    conn = Connection('localhost', 27017)
    db = conn.council
    members = db.members
    
    
    blocks = members.find()

    response['blocks'] = blocks
    return render_to_response('test.html', response)


def home(request):
    response = {}
    
    collection = connection()
    blocks = collection.distinct('date')
    
    response['blocks'] = blocks
    
    response['search'] = SearchForm()
    for block in blocks:
        print block
    return render_to_response('home.html', response)
    

def search(request, q=""):
    collection = connection()
    
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            s = solr.SolrConnection('http://localhost:8983/solr')
            raw_results = s.query(str(form.cleaned_data['q']), highlight=True, fields="features,id,snippets")
            results = [result for result in raw_results]
            full_objects = []

            for elt in results:
                obj = collection.find_one( {'_id': objectid.ObjectId(elt['id'])})
                full_objects.append(obj)
                
            s.close() # TODO make sure this closes the connection to Solr.
            return render_to_response('search.html', {'results':full_objects})
            
    return home(request)


def member(request, member):
    collection = connection()
    member_slugs = member_slugs_mapping()
    response = {}
    member = member_slugs[member]
    response['member'] = member
    
    blocks = collection.find( {'$or': [ {'yeas':member}, {'nays':member}], 'type':'contract'}, sort=[('date', ASCENDING)] )
    
    yeas = collection.find(  {'$or': [ {'yeas':member}] }, sort=[('date', ASCENDING)]  )
    
    nays = collection.find(  {'$or': [ {'nays':member}] }, sort=[('date', ASCENDING)]  )
    response['yeas'] = yeas
    response['nays'] = nays
    
    return render_to_response('member.html', response)
    
    
def meeting(request, y, m, d):
    response = {}
    
    date = datetime.datetime(int(y),int(m),int(d))
    response['date'] = date
    
    collection = connection()
    blocks = collection.find( {'date': date} )
    blocks = [ block for block in blocks]
    response['blocks'] = blocks
    
    total_spent = 0
    contracts = []
    for block in blocks:
        if block['type'] == 'contract':
            contracts.append(block['dollar_ammounts'][-1])
            total_spent += block['dollar_ammounts'][-1]

    contracts.sort()
    response['contracts'] = contracts
    response['total_spent'] = total_spent

    return render_to_response('meeting.html', response)
    
    
def item(request, item):
    collection = connection()
    response = {}
    
    id = objectid.ObjectId(item)
    block = collection.find_one( {'_id': id})
    
    
    if not 'entities' in block:
        print "calculating"
        # calais = Calais(settings.CALAIS, submitter="hello world")
        # block['entities'] = calais.analyze(block['string']).entities
        # collection.save(block)
    
    response['item'] = block
    
    meeting_items = collection.find( {'date': block['date']} )
    meeting_items_processed = []
    for item in meeting_items:
        if item['_id'] == id:
            item['selected'] = True
        
        meeting_items_processed.append(item)
    response['blocks'] = meeting_items_processed

    return render_to_response('item.html', response)
    
    
def page(request, page):
    response = {}
    
    page = int(page)
    response['page'] = page
    response['next'] = page + 1 if page < 2796 else None
    response['prev'] = page - 1 if page > 1 else None
    
    image = "http://mh-council.s3.amazonaws.com/2009council_" + str(page) + ".png"
    response['image'] = image
    
    collection = connection()
    blocks = collection.find( {'page_number': page - 1 })
    response['blocks'] = blocks
    
    return render_to_response('page.html', response)

    
def contract(request, contract):
    response = {}
    collection = connection()
    blocks = collection.find( { 'contracts':contract}, sort=[('date', ASCENDING)] )
    
    # get last block and display if it was approved or not
   
    calais = Calais(settings.CALAIS, submitter="hello world")
    
    newbloks = []
    for block in blocks:
        block['entities'] = calais.analyze(block['string']).entities
        newbloks.append(block)
        
    response['items'] = newbloks
    response['contract'] = contract
    return render_to_response('contract.html', response)
