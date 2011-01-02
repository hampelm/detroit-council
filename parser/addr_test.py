from addresses import parse_addresses
string = 'Dangerous Structures Honorable City Council: In accordance with Section 12-11-28.4 of the Building Code, hearings were held for the purpose of giving the owner or owners the opportunity to show cause why certain structures should not be demolished or otherwise made safe. After careful consideration of same, your Committee recommends that action be taken as set forth in the following resolution. Respectfully submitted, ALBERTA TINSLEY-TALABI Chairperson By Council Member Tinsley-Talabi: Resolved, That the findings and determination of the Buildings and Safety Engineering Department that certain structures on premises known as 15818 Virgil, 2725-7 Virginia Park, 8111 Warwick, 8117 Warwick, 1629 Waterman, 1635 Waterman, 15750 Westbrook, 6464 Westwood, 7639 Wetherby, 15459 Wisconsin, 4210 Woodhall and 15746-8 Woodingham, as shown in the proceedings of October 20, 2009 (J.C.C. pg. ), are in a dangerous condition and should be removed, be and are hereby approved, and be it further Resolved, That the Buildings and Safety Engineering Department be and it is hereby authorized and directed to take the necessary steps for the removal of dangerous structures at 2725-7 Virginia Park, 8111 Warwick, 8117 Warwick, 1629 Waterman, 1635 Waterman, 15750 Westbrook, 6464 Westwood, 7639 Wetherby, 15459 Wisconsin, 4210 Woodhall and 15746-8 Woodingham, and to assess the costs of same against the properties more particularly described in above mentioned proceedings of October 20, 2009), and be it further Resolved, That dangerous structure at the following location be and the same is hereby returned to the jurisdiction of the Buildings and Safety Engineering Department for the reason indicated. 15818 Virgil -- Withdraw. Adopted as follows: Yeas -- Council Members Jones, Kenyatta, Reeves, Tinsley-Talabi, Watson, and President K. Cockrel, Jr. -- 6. Nays -- None.'

print parse_addresses(string)