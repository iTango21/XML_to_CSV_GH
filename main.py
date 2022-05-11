import xml.etree.ElementTree as ET
import csv
import pandas as pd
import itertools

from pathlib import Path


df_wh = pd.read_csv('Warehouses.csv', sep=',', header=0)
df_wh.set_index('WarehouseID', inplace=True)

my_listtt = df_wh["WarehouseName"].tolist()
# print(my_listtt)

my_r = []
for r in df_wh.index:
    my_r.append(int(r.split('-')[1]))
# print(my_r)
#
# breakpoint()


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
# list_wh = ['"Ljubljana - Celovška"', '', '"Ljubljana - Slovenska"', '"Ribnica"', '"Idrija"', '"Novo Mesto"', '"Kranj"']
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
                # for t in range(1, 8):
                #     if t != 2:
                #         try:
                #             zalogape = (jjj.find(f"ZalogaPE-0{t}")).text
                #             if zalogape != '':
                #                 list_wh_add.append(list_wh[t-1:t])
                #                 list_count.append(zalogape)
                #             else:
                #                 list_count.append(0)
                #         except:
                #             list_count.append(0)
                for s in df_wh.index:
                    try:
                        zalogape = (jjj.find(s)).text

                        w = int(s.split('-')[1])
                        if zalogape != '':
                            qqq = f'"{df_wh.loc[s]["WarehouseName"]}"'
                            #print(f'{s} --> {qqq}')
                            list_wh_add.append(qqq)
                            list_count.append(zalogape)
                        else:
                            list_count.append(0)
                    except:
                        list_count.append(0)

                print(list_wh_add)
                lst_txt = str(list_wh_add).replace("['", "[").replace("']", "]").replace("', '", ", ").strip()
                print(f'{lst_txt}\n')
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

df.to_csv('output.csv', index=False, sep = ',')#, quoting=csv.QUOTE_NONE, escapechar='"') #quoting=csv.QUOTE_NONE,, escapechar=','
#df.to_csv('output.csv', index=False, sep = '\t', quoting=csv.QUOTE_NONE, escapechar='#') #quoting=csv.QUOTE_NONE,, escapechar=','
#df.to_csv('output.csv', index=False, sep=',', quoting=csv.QUOTE_NONE, escapechar='*') #quoting=csv.QUOTE_NONE,, escapechar=','
# df.to_csv('output.csv', index=False, sep=',', escapechar='*', quoting=csv.QUOTE_NONE, quotechar='#') #quoting=csv.QUOTE_NONE,, escapechar=','


# Variant SKU,Command,"""Variant Metafield: my_fields.zaloga [list.single_line_text_field]""","""Variant Metafield: my_fields.zalogape-01 [number_integer]""","""Variant Metafield: my_fields.zalogape-03 [number_integer]""","""Variant Metafield: my_fields.zalogape-04 [number_integer]""","""Variant Metafield: my_fields.zalogape-05 [number_integer]""","""Variant Metafield: my_fields.zalogape-06 [number_integer]""","""Variant Metafield: my_fields.zalogape-07 [number_integer]"""
# 9010159990146-45,MERGE,"[""Ljubljana - Celovška"", ""Ljubljana - Slovenska""]",1,2,0,0,0,0
# 9010159990153-45,MERGE,"[""Ljubljana - Celovška"", ""Ljubljana - Slovenska"", ""Novo Mesto""]",3,4,0,0,5,0
# 9010159990207-45,MERGE,"[""Ljubljana - Celovška"", ""Ljubljana - Slovenska"", ""Novo Mesto""]",1,1,0,0,1,0
# 9010159990214-45,MERGE,"[""Ljubljana - Celovška"", ""Ljubljana - Slovenska""]",3,4,0,0,0,0

# Variant SKU,Command,"""Variant Metafield: my_fields.zaloga [list.single_line_text_field]""","""Variant Metafield: my_fields.zalogape-01 [number_integer]""","""Variant Metafield: my_fields.zalogape-03 [number_integer]""","""Variant Metafield: my_fields.zalogape-04 [number_integer]""","""Variant Metafield: my_fields.zalogape-05 [number_integer]""","""Variant Metafield: my_fields.zalogape-06 [number_integer]""","""Variant Metafield: my_fields.zalogape-07 [number_integer]"""
# 9010159990146-45,MERGE,"[""Ljubljana - Celovška"", ""Ljubljana – Slovenska""]",1,2,0,0,0,0
# 9010159990153-45,MERGE,"[""Ljubljana - Celovška"", ""Ljubljana – Slovenska"", ""Novo Mesto""]",3,4,0,0,5,0
# 9010159990207-45,MERGE,"[""Ljubljana - Celovška"", ""UA_V-V"", ""UA_UA""]",1,0,0,0,0,0
# 9010159990214-45,MERGE,"[""Ljubljana - Celovška"", ""Kranj""]",3,0,0,0,0,77



def main():
    pass


if __name__ == "__main__":
    main()
