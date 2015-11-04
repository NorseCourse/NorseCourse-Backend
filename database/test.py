import pandas as pd
import re

data = pd.DataFrame.from_csv('data.csv', sep=None,index_col=None)


lab = "BIO-364L-A"

for x in data['section_name']:
	if x in lab:
		print(x)
		
if "BIO-364L" in "BIO-364L-A01":
	print('here')