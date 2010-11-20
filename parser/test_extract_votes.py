from helpers import extract_votes

block1 = {}
block1['string'] = 'Finance Department Purchasing Division September 16, 2009 Honorable City Council: The Purchasing Division of the Finance Department recommends a Contract with the following firm(s) or person(s): 2797973 -- 100% City Funding -- To provide Belle Isle - Scott Fountain Renova- tions -- Grunwell-Cashero Co., 1041 Major, Detroit, MI 48217 -- Contract Period: Upon Notice to Proceed -- Until Completion of the Project -- Contract Amount Not to Exceed: $300,000.00. Recreation. (Contract held by Council Member Sheila M. Cockrel during recess week of August 10, 2009) Respectfully submitted, CHRISTINA LADSON Interim Director Finance Dept./Purchasing Div. By Council Member Watson: Resolved, That Contract No. 2797973 referred to in the foregoing communica- tion, dated July 30, 2009, be hereby and is approved. Adopted as follows: Yeas -- Council Members S. Cockrel, Collins, Jones, Kenyatta, Reeves, Tinsley-Talabi, Watson, and President K. Cockrel, Jr. -- 8. Nays -- None. *WAIVER OF RECONSIDERATION (No. 36), per motions before adjournment.'

block = extract_votes(block1)
yeas = ['S. Cockrel', 'Collins', 'Jones', 'Kenyatta', 'Reeves', 'Tinsley-Talabi', 'Watson', 'K. Cockrel, Jr.']
nays = []

if block['nays'] != nays:
    assert(False)

for person in block['yeas']:
    if person not in yeas:
        assert(False)
    


block2 = {}
block2['string'] = 'Finance Department Purchasing Division September 16, 2009 Honorable City Council: The Purchasing Division of the Finance Department recommends a Contract with the following firm(s) or person(s): 2797973 -- 100% City Funding -- To provide Belle Isle - Scott Fountain Renova- tions -- Grunwell-Cashero Co., 1041 Major, Detroit, MI 48217 -- Contract Period: Upon Notice to Proceed -- Until Completion of the Project -- Contract Amount Not to Exceed: $300,000.00. Recreation. (Contract held by Council Member Sheila M. Cockrel during recess week of August 10, 2009) Respectfully submitted, CHRISTINA LADSON Interim Director Finance Dept./Purchasing Div. By Council Member Watson: Resolved, That Contract No. 2797973 referred to in the foregoing communica- tion, dated July 30, 2009, be hereby and is approved. Adopted as follows: Yeas -- Council Members S. Cockrel, and Collins -- 2. Nays -- Council Members Jones, Kenyatta, Reeves, Tinsley-Talabi, Watson, and President K. Cockrel, Jr. -- 8. *WAIVER OF RECONSIDERATION (No. 36), per motions before adjournment.'

block = extract_votes(block2)
nays = ['Jones', 'Kenyatta', 'Reeves', 'Tinsley-Talabi', 'Watson', 'K. Cockrel, Jr.']
yeas = ['S. Cockrel', 'Collins']

for person in block['nays']:
    if person not in nays:
        print person
        assert(False)

for person in block['yeas']:
    if person not in yeas:
        print person
        assert(False)
        
        
        
block3 = {}
block3['string'] = ''

