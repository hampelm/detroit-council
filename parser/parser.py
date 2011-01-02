import codecs
import linecache 
import re
import solr
import sys
import time

from pymongo import Connection
from dateutil import parser
from django.template.defaultfilters import slugify

from blockparser import extract_planning, buildings_and_safety
from contracts import extract_contract
from helpers import *
from resolutions import extract_resolution
filename = '2009council.txt'
f = open(filename, 'rb')

text = []
text_as_str = []

def setattr(block_idx, key, val):
    text[block_idx][key] = val


def line_is_separator(line, idx):
    '''
    Test if the current line separates meeting items.
    There are several separators:
    * Dashes (the most common)
    * Page breaks (harder to detect)
    '''
    tests = ["----------\n", ' PUBLIC COMMENTS', 'CITY COUNCIL------', 'CITY COUNCIL------']
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
Break the file into blocks, and store them in text[] 
Blocks are delineated in the text by separators (see line_is_separator)
Each block should be a distinct meeting item
Also extracts metadata, like page numbers and dates.

Block format:
    lines: a list of each line
    string: all lines as one string
    page_number
    date (datetime)
    type (to committee, resolution, etc)

'''
def first_pass(f, text):
    page_number = 1
    skip_next = False
    date = ''
    
    block = {}
    block['lines'] = []
    block['page_number'] = 1
    
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
            block['title'] = block['lines'][0]
        
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
                        
    return text
                
                
    
'''
Create a parallel representation of the blocks where every
line is combined into one big string.

TODO: repair hyphenation
'''
def block_string_generator(text):
    for block_index, block in enumerate(text):
        block_text_as_str = ''
        for line in block['lines']:
            block_text_as_str = block_text_as_str + ' ' + line
        
        text[block_index]['string'] = block_text_as_str
        
    return text
    
'''
MAIN SCANNER

Parse through the block to attempt to detect what type of
information it contains (invocation, resolutions, ...)
'''
def scanner(text):
    for block_index, block in enumerate(text):
    
        '''
        First we see what we can detect from the block as
        one big string.
        '''
        block_as_str = text[block_index]['string']
        
        
        
        '''
        PERMITS
        '''
        if block['lines'][0] == 'Permit':
            setattr(block_index, 'type', 'permit') 
            block = extract_votes(block)
    
        
        '''
        P&D
        '''
        if block['lines'][0] == 'Planning & Development Department':
            block = extract_planning(block)
            # setattr(block_index, 'type', 'planning')
        
        '''
        Buildings & Safety
        '''
        if block['lines'][0] == 'Buildings and Safety':
            block = buildings_and_safety(block)
            
            if 'Emergency Demolition' in block['string']:
                setattr(block_index, 'type', 'emergency demolition')        
    
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
    return text


# Save the stuff to Mongo
def save_to_mongo(text):
    connection = Connection('localhost', 27017)
    db = connection.council
    collection = db.blocks
    collection.remove({}) # clear out all the old data

    for block in text:
        block = repair_text(block)
        collection.insert(block)

    
def save_to_solr():
    connection = Connection('localhost', 27017)
    db = connection.council
    collection = db.blocks
    
    # Save the stuff to solr
    batch = []
    everything = collection.find()
    BAD_MAP = ''.join([chr(x) for x in range(32) + [124]])
    for elt in everything:
        # first strip out control chars, which solr doesn't like
        body = elt['string']
        batch.append({'id': elt['_id'], 'features': body })
    
    s = solr.SolrConnection('http://localhost:8983/solr')
    s.delete(queries=['*:*'])
    s.add_many(batch)
   
   
# Generate the mapping of members to slugs.
# everyone votes yes at least once.
def generate_member_slugs():
    connection = Connection('localhost', 27017)
    db = connection.council
    collection = db.blocks
    memberdb = db.members
    
    memberdb.remove({}) # clear out all the old data
    
    members = collection.distinct('yeas')
    for member in members:
        record = {}
        record[slugify(member)] = member
        memberdb.insert(record)


# Run the actual import

# text = first_pass(f, text)
# text = block_string_generator(text)
# text = scanner(text)
# save_to_mongo(text)
# save_to_solr()
generate_member_slugs()
