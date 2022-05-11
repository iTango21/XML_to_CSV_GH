import xml.etree.ElementTree as ET
import csv
import pandas as pd
import itertools

from pathlib import Path


cols = [
    'Variant SKU',
    'Command',
    '"Variant Metafield: my_fields.zaloga [list.single_line_text_field]"',
    '"Variant Metafield: my_fields.zalogape-01 [number_integer]"',
    '"Variant Metafield: my_fields.zalogape-03 [number_integer]"',
    '"Variant Metafield: my_fields.zalogape-04 [number_integer]"',
    '"Variant Metafield: my_fields.zalogape-05 [number_integer]"',
    '"Variant Metafield: my_fields.zalogape-06 [number_integer]"',
    '"Variant Metafield: my_fields.zalogape-07 [number_integer]"'
]


rows = []

"""
Warehouse ID	Warehouse Name
ZalogaPE-01	    Ljubljana - Celovška
ZalogaPE-03	    Ljubljana – Slovenska
ZalogaPE-04	    Ribnica
ZalogaPE-05	    Idrija
ZalogaPE-06	    Novo Mesto
ZalogaPE-07	    Kranj
"""
#list_wh = ['"Ljubljana - Celovška"', '', '"Ljubljana – Slovenska"', '"Ribnica"', '"Idrija"', '"Novo Mesto"', '"Kranj"']
list_wh = ['"Ljubljana - Celovška"', '', '"Ljubljana - Slovenska"', '"Ribnica"', '"Idrija"', '"Novo Mesto"', '"Kranj"']
list_wh_add = []
list_count = []

tree = ET.parse("test.xml")
root = tree.getroot()


ttt = tree.findall('Artikel')

for www in ttt:
    sss = www.findall('Velikostne_st')
    for zzz in sss:
        yyy = zzz.findall('Velikost')
        for jjj in yyy:
            ean = jjj.find('EAN').text
            sezona = jjj.find("Sezona").text

            if (ean is not None) & (sezona is not None):
                for t in range(1, 8):
                    if t != 2:
                        try:
                            zalogape = (jjj.find(f"ZalogaPE-0{t}")).text
                            if zalogape != '':
                                list_wh_add.append(list_wh[t-1:t])
                                list_count.append(zalogape)
                            else:
                                list_count.append(0)
                        except:
                            list_count.append(0)

                lst_txt = str(list_wh_add).replace("['", "").replace("']", "").strip()
                # print(lst_txt)
                #["Ljubljana - Celovška", "Ljubljana - Slovenska"]
                rows.append({'Variant SKU': f'{ean}-{sezona}',
                             'Command': 'MERGE',
                             '"Variant Metafield: my_fields.zaloga [list.single_line_text_field]"': f'{lst_txt}',
                             '"Variant Metafield: my_fields.zalogape-01 [number_integer]"': list_count[0],
                             '"Variant Metafield: my_fields.zalogape-03 [number_integer]"': list_count[1],
                             '"Variant Metafield: my_fields.zalogape-04 [number_integer]"': list_count[2],
                             '"Variant Metafield: my_fields.zalogape-05 [number_integer]"': list_count[3],
                             '"Variant Metafield: my_fields.zalogape-06 [number_integer]"': list_count[4],
                             '"Variant Metafield: my_fields.zalogape-07 [number_integer]"': list_count[5]
                             })

                list_wh_add = []
                list_count = []


df = pd.DataFrame(rows)#, columns=cols)

df.to_csv('output.csv', index=False, sep = ',')#, quoting=csv.QUOTE_NONE, escapechar='#') #quoting=csv.QUOTE_NONE,, escapechar=','
#df.to_csv('output.csv', index=False, sep = '\t', quoting=csv.QUOTE_NONE, escapechar='#') #quoting=csv.QUOTE_NONE,, escapechar=','
#df.to_csv('output.csv', index=False, sep=',', quoting=csv.QUOTE_NONE, escapechar='*') #quoting=csv.QUOTE_NONE,, escapechar=','
# df.to_csv('output.csv', index=False, sep=',', escapechar='*', quoting=csv.QUOTE_NONE, quotechar='#') #quoting=csv.QUOTE_NONE,, escapechar=','


def main():
    pass


if __name__ == "__main__":
    main()
