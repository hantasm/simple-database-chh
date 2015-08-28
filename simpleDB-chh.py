# simpleDB developed by Chenghu He

import sys

for line in sys.stdin:
    if line == 'END\n' or line == None:
         break
    print(line[:-1])
    
