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
block3['string'] = 'INTERNAL OPERATIONS STANDING COMMITTEE The following Finance Department/ Purchasing Division Contracts were approved through the recess procedure for the week of December 15, 2008. Finance Department Purchasing Division December 11, 2008 Honorable City Council: The Purchasing Division of the Finance Department recommends a Contract with the following firms or persons: 2782141 -- 100% City Funding -- Heavy Duty Truck Repair -- RFQ. #27435, Par. #2884 -- All Type Truck & Trailer Repair (Supplier 3 of 3), 23660 Sherwood, Warren, MI 48091 -- Contract period: December 15, 2008 through December 14, 2010, with two (2)-one (1) year renewal options -- (2) Items -- Unit prices range from: $49.50/hr. to $49.50/hr. -- Lowest acceptable bid -- Estimated cost: $158,400.00/2 years. GENERAL SERVICES. Respectfully submitted, MEDINA NOOR Director Finance Dept./Purchasing Division By Council Member Kenyatta: Resolved, That Contract No. 2782141 referred to in the foregoing communication dated December 11, 2008 be hereby and is approved. Adopted as follows: Yeas -- Council Members S. Cockrel, Collins, Jones, Kenyatta, Tinsley-Talabi, Watson, and President Conyers -- 7. Nays -- None.'

block = extract_votes(block3)
yeas = ['S. Cockrel', 'Collins', 'Jones', 'Kenyatta', 'Tinsley-Talabi', 'Watson', 'Conyers']
nays = []

for person in block['nays']:
    if person not in nays:
        print person
        assert(False)

for person in block['yeas']:
    if person not in yeas:
        print person
        assert(False)

print "No nays 2 passed"
