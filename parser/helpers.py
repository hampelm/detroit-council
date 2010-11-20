import sys
import re


'''
Regular expression patterns
'''
# Identifies strings that represent money.
MONEY_PATTERN = re.compile(r'\$\d+[0123456789,]+\.\d{2}')


'''
Fixes hyphens and other issues.
'''
def repair_text(block):
    hyphenated_pattern = re.compile(r'\w+-\s\w+')
    for match in hyphenated_pattern.findall(block['string']):
        replacement = match.replace('- ', '')
        block['string'] = block['string'].replace(match, replacement)
        
    return block


def format_html(block):
    string = block['string']
    
    whereas = r'Whereas,*\.'
    for match in whereas.findall(string):
        string.replace(match, '<p>' + match + '</p>')
        
    block['formatted'] = string
    return block

'''
Extract the votes from a block
'''
def name_cleanup(text):
    replacements = [
        (', Jr.', '; Jr.'), 
        ('and ', ''), 
        (' Council Members', ''), 
        ('President ', ''),
        ('Pro Tem Conyers', 'Conyers'), 
        ('Pro Tem. Conyers', 'Conyers'), 
        ('Pro Tem Watson', 'Watson'),
        ('Pro Tem.Watson', 'Watson'),
        ('Pro Tem. Watson', 'Watson'),
        ('Pro-Tem Watson', 'Watson'),
        ('Tinsley- Talabi', 'Tinsley-Talabi'),
    ]
    
    for pattern in replacements:
        text = text.replace(pattern[0], pattern[1])
            
    return text
    


def extract_votes(block):
    '''
    The votes always start with 'Adopted as follows:' and run to the end
    of the block.
    
    The easier way to do this would be to split yeas and nays --
    then check what council members are in each. Much less fragile (I think)
    For example:
    for member in council:
        if member in yeas:
            yes_votes.append(member)
        if member in nays:
            no_votes.append(member)
    '''
    votes_start = block['string'].find('Adopted as follows:')
    if votes_start == -1:
        # there is no vote in this block
        return block
    
    # Separate the yeas from the nays
    # Cut out some excess text
    votes_text = block['string'][votes_start:]
    votes_text = name_cleanup(votes_text)

    # Figure out where the yeas and nays start
    yeas_start = votes_text.find('Yeas')
    nays_start = votes_text.find('Nays')
    
    # Split them apart
    yeas_text = votes_text[yeas_start:nays_start]
    yeas_text = yeas_text.split('--')[1]
    
    nays_text = 'None'
    if nays_start is not -1:
        nays_text = votes_text[nays_start:]
        nays_text = nays_text.split('--')[1]
    
    
    if 'None' not in nays_text:
        nays = nays_text.split(',')
    else:
        nays = []
        
    if 'None' not in yeas_text:
        yeas = yeas_text.split(',')
    else:
        yeas = []
    
    # More general cleanup
    if yeas != []:
        yeas = [name.strip() for name in yeas]
        yeas = [name.replace(';',',') for name in yeas]        
    
    if nays != []:
        nays = [name.replace(';',',') for name in nays]
        nays = [name.strip() for name in nays]
        
        
    # now store them by voter:
  #  block['votes_by_member'] = {}
 #   for member in yeas:
 #       block['votes_by_member'][member] = 'Yea'
 #   for member in nays:
 #       block['votes_by_member'][member] = 'Nay'
        
    block['yeas'] = yeas
    block['nays'] = nays

    # Sanity check.
    if len(yeas) + len(nays) < 5:
        # That's not a quorum.
        assert(False)
    
    return block



''' 
Given a block from the text, finds the detroit-based addresses
(only those that are in 48***)
'''
def find_address(block):
    addresses = []
    bits = block['string'].split(' -- ')
    for elt in bits:
        '''
        The ZIP is nearly always the last 5 digits in the string.
        '''
        if elt[-5:-3] == '48':
            addresses.append(elt)
            '''
            These are some extra checks to make sure the is is actually an 
            address.
            '''
            # pieces = elt.split(',')
            # if pieces[-1][0:5] == 'MI 48':
            #     print elt
    
    if len(addresses) > 1:
        '''
        Return false if there are many addresses
        '''
        
        return False
    elif len(addresses) == 0:
        '''
        Return the empty string if none were found
        '''
        return ''       
    else:
        return addresses[0]
        
    