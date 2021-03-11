

import asuciasuci as asuci 
import utils 

bills = utils.load_json(asuci.pBILLS, [])

for b in bills:
    print(b.get('date_presented'))
    print(b.get('date_voted'))