import re
from helpers import find_address, extract_votes
import helpers

def extract_contract(block):
    block_as_str = block['string']
    
    # extract the contract number
    contracts = []
    contract_pattern = r'Contract No\. (\d{4}\d+)'
    contract_pattern = re.compile(contract_pattern)
    for m in contract_pattern.findall(block['string']):
        contracts.append(m)
    block['contracts'] = contracts
    
    # extract the addresses        
    block['address'] = find_address(block)
  
    #extract the dollar amounts
    dollars = []
    for m in helpers.MONEY_PATTERN.findall(block['string']):
        m = m.replace('$','')
        m = m.replace(',','')
        m = float(m)
        dollars.append(m)
    
    if len(dollars) > 2:
        # If there are more than two dollar amounts, this probably is 
        # being sent off to committee.
        block['type'] = 'to committee'
    
        # TODO -- parse out what committee.

    elif len(dollars) == 2:
        # If there are two dollar amounts, it needs human intervention
        # to know what's up. It could be two contracts for referral, or
        # an ammended contract.
        block['type'] = 'contract'
        block['address'] = find_address(block)
        block = extract_votes(block)
        block['review'] = True
        
    
    elif len(dollars) == 1:
        # One ammount almost certainly means its a contract.
        block['type'] = 'contract'
        block['address'] = find_address(block)
        block['cost'] = dollars[0]
        block = extract_votes(block)
    
    else:
        # Hm, not sure what it could be.
        block['type'] = 'unknown'
        block['review'] = 'True'
        
    #if ('BEING REFERRED' in block_as_str) or ('TO BE REFERRED' in block_as_str) or ('WERE REFERRED' in block_as_str):
    #    block['type'] = 'referral'

    block['dollars'] = dollars
    
    return block