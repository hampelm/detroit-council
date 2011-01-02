# This Python file uses the following encoding: utf-8
import re
from helpers import find_address, extract_votes, DIRECTIONS
import helpers

def extract_case(block):
    return block


'''
Extract information about planning department decisions.
'''
def extract_planning(block):    
    start = block['string'].find('Re: ')
    ends = ['The City of Detroit acquired as ', 'The above named']
    
    for string in ends:
        end = block['string'].find(string)
        if start != -1 and end != -1:
            subject = block['string'][start:end]
            block['details'] = subject
        
    
    # Petition No. 3212
    petitions = re.search('Petition No. (\d+)', block['string'])
    try:    
        block['petition'] = int(petitions.group(0))
    except:
        pass
    
    block = extract_votes(block)
    
    return block
        
'''
Buildings and safety engineering
'''
          
def buildings_and_safety(block):
    '''
    Re: Address: 4400 Bewick.
    Re: Dangerous Buildings.
    Re: Address: 9324-6 W. Fort
    '''
    
    for line in block['lines']:
        if 'Re: ' in line:
            continue
            
        if 'Re: Address' in line:
            for direction in helpers.DIRECTIONS:
                # strip the periods from directions
                line = line.replace(direction + '.', direction)
            block['address'] = line.split('.')[0]
            
        if 'Re: Dangerous Buildings' in line:
            block['type'] = 'dangerous buildings'
    
    block = extract_votes(block)
    return block
    
      
'''
Re: Departmental Recommendation.
Petition No. 3184 -- Lola's, request
Outdoor Café Permit at 1427
Randolph in Harmonie Park.
'''

