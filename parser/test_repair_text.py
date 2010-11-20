from helpers import repair_text

block = {}
block['string'] = 'there is a hyph- enated word'

to_test = repair_text(block)

if to_test['string'] != 'there is a hyphenated word':
    print to_test['string']
    assert(False)