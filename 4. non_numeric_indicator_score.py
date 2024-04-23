import _number_of_country


number_country = _number_of_country.number_country
read_base = 'indicator_score.xlsx'
read_add = 'special_columns_test.xlsx'
output = 'indicator_score_final.xlsx'

import pandas as pd

insc = pd.read_excel(read_base)
sinsc = pd.read_excel(read_add).drop([0, number_country+1]).reset_index(drop=True)

for i in sinsc.columns:
    if i not in insc.columns:
        insc[i] = sinsc[i]
    print(insc[i])

insc.to_excel(output, index=False)