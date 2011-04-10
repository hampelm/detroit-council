from helpers import extract_votes, name_cleanup

text = 'President Pro Tem Conyers, Pro-Tem Watson'
text = name_cleanup(text)
if text.find('Pro Tem') != -1:
    assert(False)

if text.find('President') != -1:
    assert(False)
print "Name cleanup passed"

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
print "No nays passed"


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
        
print "Mixed votes passed"

        
block3 = {}
block3['string'] = 'Finance Department Purchasing Division April 28, 2009 Honorable City Council: The Purchasing Division of the Finance Department recommends a Contract with the following firms or persons: 2778457 -- 100% State Funding -- To provide Job Readiness/Job Search -- Foundation for Behavioral Resources, 600 South Lincoln Street, Augusta, MI 49012 -- Contract period: October 1, 2008 through September 30, 2009 -- Contract amount not to exceed: $900,000.00. DWDD. Respectfully submitted, MEDINA NOOR Director Finance Dept./Purchasing Division By Council Member Collins: Resolved, That Contract No. 2778457 referred to in the foregoing communication dated April 28, 2009, be hereby and is approved. Not adopted as follows: Yeas -- Council Members S. Cockrel, Collins, Reeves, and Tinsley-Talabi -- 4. Nays -- Council Members Jones, Kenyatta, Watson, and President Conyers -- 4.'

block = extract_votes(block3)
yeas = ['S. Cockrel', 'Collins', 'Reeves', 'Tinsley-Talabi']
nays = ['Jones', 'Kenyatta', 'Watson', 'Conyers']

for person in block['nays']:
    if person not in nays:
        print person
        assert(False)

for person in block['yeas']:
    if person not in yeas:
        print person
        assert(False)

print "Mixed votes 2 passed"
