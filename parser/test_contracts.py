from contracts import extract_contract

block1 = {}
block1['string'] = 'Finance Department Purchasing Division September 16, 2009 Honorable City Council: The Purchasing Division of the Finance Department recommends a Contract with the following firm(s) or person(s): 2797973 -- 100% City Funding -- To provide Belle Isle - Scott Fountain Renova- tions -- Grunwell-Cashero Co., 1041 Major, Detroit, MI 48217 -- Contract Period: Upon Notice to Proceed -- Until Completion of the Project -- Contract Amount Not to Exceed: $300,000.00. Recreation. (Contract held by Council Member Sheila M. Cockrel during recess week of August 10, 2009) Respectfully submitted, CHRISTINA LADSON Interim Director Finance Dept./Purchasing Div. By Council Member Watson: Resolved, That Contract No. 2797973 referred to in the foregoing communica- tion, dated July 30, 2009, be hereby and is approved. Adopted as follows: Yeas -- Council Members S. Cockrel, Collins, Jones, Kenyatta, Reeves, Tinsley-Talabi, Watson, and President K. Cockrel, Jr. -- 8. Nays -- None. *WAIVER OF RECONSIDERATION (No. 36), per motions before adjournment.'

cost1 = float('300000.00')
address1 = 'Grunwell-Cashero Co., 1041 Major, Detroit, MI 48217'

results = extract_contract(block1)
print results['cost']
assert(results['cost'] == cost1)
assert(results['address'] == address1)
assert(results['type'] == 'contract')



'''
This block is a contract that is being amended.
'''
block2 = {}
block2['string'] = 'Finance Department Purchasing Division February 17, 2009 Honorable City Council: The Purchasing Division of the Finance Department recommends a Contract with the following firms or persons: 2725593 -- (Change Order No. #01) -- (SW-549) -- Southwest Water Treatment Plant Intake Improvements and Rehab- ilitation -- Posen Construction, Inc., 2111 Woodward Ave., Ste. 507, Detroit, MI 48201 -- Contract period: Time extension of 280 calendar days (July 24, 2007 through May 1, 2009) -- Contract increase: $761,540.00 -- Contract amount not to exceed: $5,544,037.98. DWSD. Respectfully submitted, MEDINA NOOR Director Finance Dept./Purchasing Division By Council Member Tinsley-Talabi: Resolved, That Contract No. P.O. #2725593 referred to in the foregoing communication dated February 17, 2009, be hereby and is approved. Adopted as follows: Yeas -- Council Members S. Cockrel, Kenyatta, Reeves, Tinsley-Talabi, and President Conyers -- 6. Nays -- Council Member Watson -- 1.'

address2 = 'Posen Construction, Inc., 2111 Woodward Ave., Ste. 507, Detroit, MI 48201'

results = extract_contract(block2)
assert(results['address'] == address2)
assert(results['review'] == True)


'''
This is not actually a contract -- it's a set of contracts being sent to 
committee for review.
'''
block3 = {}
block3['string'] = "RESOLUTION By ALL COUNCIL MEMBERS: THE FOLLOWING ITEM IS BEING REFERRED TO THE BUDGET, FINANCE AND AUDIT STANDING COMMITTEE: FINANCE DEPARTMENT/PURCHASING DIVISION 1. Submitting reso. autho. Contract No. 2747087 -- (Change Order No. 1) -- 100% City Funding -- To Fund the Detroit Wayne County Port Authority's Administrative Budget -- Detroit/Wayne County Port Authority, 8109 E. Jefferson Ave., Detroit, MI 48226 -- Contract Period: July 1, 2008 through June 30, 2009 -- Contract Increase: $250,000.00 -- Contract Amount Not to Exceed: $500,000.00. Finance. Adopted as follows: Yeas -- Council Members S. Cockrel, Collins, Jones, Kenyatta, Tinsley-Talabi, Watson, and President Conyers -- 7. Nays -- None."

results = extract_contract(block3)
assert(results['type'] == 'referral')
