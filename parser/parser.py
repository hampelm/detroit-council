import codecs
import linecache 
import re
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
        next = linecache.getline(filename, idx+1)
        if 'WAIVER' not in next:
            return True
        
    return False


def skip_next():
    return False


'''
Break the file into chunks, and store them in text[] 
Chunks are delineated in the text by separators (see line_is_separator)
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
        '''
        dateline_pattern = r'(\d+ 2009)'
        r = re.compile(dateline_pattern)
        match = r.search(line)
        if match:
            '''
            This is a dateline. It tells us what page we are on, 
            and what day the meeting was held.
            '''
            if (len(line.split(' ')) == 4) and line.rstrip()[-1] == '9':
                line = line.strip()
                datebits = line.split(' ')
                datestr = datebits[0].lstrip() + ' ' + datebits[1] + ' ' + datebits[3].rstrip()
                print datestr
                print type(datestr)
                date = parser.parse(datestr)
                
                
                
                match =  match.group(1)
                page_number = match.split(' ')[0]
                skip_next = True # The next line is some gibberish
        else:
            '''
            This is not a dateline.
            Continue with normal import.
            '''
            if not skip_next and not (line == "Journal of the City Council") and not (line == "(OFFICIAL)"):
                
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
                    
            else:
                skip_next = False # reset the skip_next so we continue.
                
    
'''
Create a parallel representation of the blocks where every
line is a separate string.

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
    
    if 'closed session' in block_as_str:
        setattr(block_index, 'type', 'closed session') 
        block = extract_votes(block)
    
    '''
    CONTRACTS
    Having 'Contract No.' in the string means this might be a contract.
    but it also could be a set of contracts being passed off to a 
    committee for evaluation     
    '''    
    if 'Contract No.' in block_as_str:
        block = extract_contract(block)  
        text[block_index] = block 
        
    elif 'RESOLVED, Th' in block_as_str or 'Resolved, Th' in block_as_str:
        block = extract_resolution(block) 
        
    else:
        '''
        After seeing what we can get from the block as one big string,
        we go line by line to try to suss out its content.
        '''
        
        for line in block['lines']:
        
            if line == "Invocation":
                # so this is the invocation           
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
            
                # print invocation
            
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
   
   
# Generate the mapping of members to slugs
members = collection.distinct('yeas')
db = connection.members
for member in members:
    record = {}
    record[slugify(member)] = member
    collection.insert(record)
