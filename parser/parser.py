import codecs
import linecache 
import re
import solr
import sys
import time

from pymongo import Connection
from dateutil import parser
from django.template.defaultfilters import slugify

from helpers import *
from contracts import extract_contract
from resolutions import extract_resolution
filename = '2009council.txt'
f = open(filename, 'rb')

text = []
text_as_str = []
block = {}
block['lines'] = []
block['page_number'] = 1


def setattr(block_idx, key, val):
    text[block_idx][key] = val


def line_is_separator(line, idx):
    '''
    Test if the current line separates meeting items.
    There are several separators:
    * Dashes (the most common)
    * Page breaks (harder to detect)
    '''
    tests = ["----------\n", ' PUBLIC COMMENTS']
    for test in tests:
        if line == test:
            return True
            
    '''
    If the line is a page break, then the next line might be the start
    of a new block. Grr.
    
    Here are a couple tests that try to find that.
    '''
    if 'Nays -- None' in line:
        next = linecache.getline(filename, idx+2)        
        if 'WAIVER' not in next:
            return False
        
    return False
    # http://127.0.0.1:8000/page/168
    # http://127.0.0.1:8000/page/170
    
    
def is_date(line):
    dateline_pattern = r'(\d+ 2009)'
    r = re.compile(dateline_pattern)
    match = r.search(line)
    if match:
        # checks to see if the line splits into four parts,
        # and that the last ends in 9 (for 2009)
        # will need to be edited for other years
        if (len(line.split(' ')) == 4) and line.rstrip()[-1] == '9':
            return True

    
def extract_date(line):
    '''
    Uses dateutil to parse the date of a meeting from a line.
    Not useful for other types of dates.
    '''
    line = line.strip()
    datebits = line.split(' ')
    datestr = datebits[0].lstrip() + ' ' + datebits[1] + ' ' + datebits[3].rstrip()
    print datestr # debug
    return parser.parse(datestr)
    
    
def extract_invocation(block):
    invocation = { } 
    invocation_text = ''
    address_start = 0
    for position, line in enumerate(block['lines']):
        if line == 'Invocation':
            pass
        elif line.isupper():
            address_start = position
            break
        else:
            invocation_text = invocation_text + ' ' + line

    invocation['speaker'] = block['lines'][address_start]
    invocation['church'] = block['lines'][address_start+1]
    address_block = block['lines'][address_start+2:]
    address = ''
    for line in address_block:
        address = address + ' ' + line

    invocation['address'] = address.lstrip()
    invocation['text'] = invocation_text.lstrip() 
    
    return invocation


'''
Break the file into chunks, and store them in text[] 
Chunks are delineated in the text by separators (see line_is_separator)
Each chunk should be a distinct meeting item
Also extracts metadata, like page numbers and dates.
'''
page_number = 1
skip_next = False
date = ''
for idx, line in enumerate(f):
    line = line.decode('iso-8859-1')
    
    if line_is_separator(line, idx):
        '''
        If the line is a divider, we are at the end of a block.
        Close this one off and save it to the text.
        ''' 
        if line == ' PUBLIC COMMENTS':
            block['lines'].append(line.rstrip('\n').lstrip())

        block['type'] = 'unknown' # mark as unknown for later processing
        block['date'] = date
        
        text.append(block)
        block = {}
        block['lines'] = []
        block['page_number'] = page_number
        
    else:    
        '''
        We are already inside a block, or have just begun a new one.
        
        First, check if the line is a dateline
        Datelines have the pattern [page number][space][year]
        eg
        November 20 2727 2009
        where 2727 is the page number
        '''
        
        if is_date(line):
            date = extract_date(line)

            try:
                page_number = line.split(' ')[-2]
                page_number = int(page_number)
            except:
                pass
            
            skip_next = True # The next line is some gibberish
            
        else:
            '''
            This is not a dateline.
            '''
            
            
            # Make sure this isn't the beginning of a meeting.
            if (line == "Journal of the City Council") or (line == "(OFFICIAL)"):
                skip_next = True
            
            if skip_next:
                # do nothing.
                # reset the skip_next so we continue.
                skip_next = False 
                    
            else:
                # Make sure we cut out all the errant printers marks
                printers_pattern = r'(^\d{3}\d+ .+ Page)'
                r = re.compile(printers_pattern)
                match = r.search(line)
                if match:
                    match = match.group(1)
                else:
                    '''
                    If the line is not a dateline, printers mark, or some
                    other gibberish, it gets imported
                    '''
                    block['lines'].append(line.rstrip('\n'))
                
                
    
'''
Create a parallel representation of the blocks where every
line is combined into one big string.

TODO: repair hyphenation
'''
for block_index, block in enumerate(text):
    block_text_as_str = ''
    for line in block['lines']:
        block_text_as_str = block_text_as_str + ' ' + line
        
    text[block_index]['string'] = block_text_as_str



'''
MAIN SCANNER

Parse through the block to attempt to detect what type of
information it contains (invocation, resolutions, ...)
'''
for block_index, block in enumerate(text):
    
    '''
    First we see what we can detect from the block as
    one big string.
    '''
    block_as_str = text[block_index]['string']
    
    
    '''
    CLOSED SESSIONS
    We can't get much from these.
    '''
    if 'closed session' in block_as_str:
        setattr(block_index, 'type', 'closed session') 
        block = extract_votes(block)
    
    
    if 'Contract No.' in block_as_str:
        '''
        CONTRACTS
        Having 'Contract No.' in the string means this might be a contract.
        but it also could be a set of contracts being passed off to a 
        committee for evaluation     
        '''    
        block = extract_contract(block)  
        text[block_index] = block 
        
    elif ('RESOLVED, Th' in block_as_str) or ('Resolved, Th' in block_as_str):
        '''
        GENERAL RESOLUTIONS
        These have "RESOLVED, ..." in them.
        '''
        
        block = extract_resolution(block) 
        
    else:                
        '''
        LINE BY LINE PARSING
        After seeing what we can get from the block as one big string,
        we go line by line to try to suss out its content.
        '''
        for line in block['lines']:
        
            '''
            INVOCATION
            '''
            if line == "Invocation":
                invocation = extract_invocation(block)
            
            
            if line.isupper():
                # TODO 
                pass


# Save the stuff to Mongo
connection = Connection('localhost', 27017)
db = connection.council
collection = db.blocks
collection.remove({}) # clear out all the old data

for block in text:
    block = repair_text(block)
    collection.insert(block)
    
    
# Save the stuff to solr
batch = []
everything = collection.find()
for elt in everything:
    batch.append({'id': elt['_id'], 'features': elt['string'] })
    
s = solr.SolrConnection('http://localhost:8983/solr')
s.delete(queries=['id:*'])
s.add_many(batch)
   
   
# Generate the mapping of members to slugs
members = collection.distinct('yeas')
db = connection.members
for member in members:
    record = {}
    record[slugify(member)] = member
    collection.insert(record)
