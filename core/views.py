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
    


#======= Views
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
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            s = solr.SolrConnection('http://localhost:8983/solr')
            raw_results = s.query('features:' + str(form['q']), highlight=True, fields="features,id,snippets")
            results = [result for result in raw_results]
            for elt in results:
                print elt
            return render_to_response('search.html', {'results':results})


def member(request, member):
    collection = connection()
    blocks = collection.find( {'$or': [ {'yeas':member}, {'nays':member}], 'type':'contract'}, sort=[('date', ASCENDING)] )
    
    return render_to_response('member.html', {'blocks': blocks, 'member':member})
    
    
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
            contracts.append(block['dollars'][-1])
            total_spent += block['dollars'][-1]

    contracts.sort()
    response['contracts'] = contracts
    response['total_spent'] = total_spent

    return render_to_response('meeting.html', response)
    
    
def item(request, y, m, d, item):
    collection = connection()
    block = collection.find_one( {'_id': objectid.ObjectId(item)})
    print block
    return render_to_response('item.html', {'item':block })
    
    
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
