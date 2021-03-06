import xml.etree.ElementTree as ET
import csv
import pandas as pd
import json
from pathlib import Path
import time
from datetime import datetime

start_time = time.time()

with open("config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

file_log = jsonObject['file_log']
file_xml = jsonObject['file_xml']
file_csv = jsonObject['file_csv']

path_log = file_log

df_wh = pd.read_csv('Warehouses.csv', sep=',', header=0)
df_wh.set_index('WarehouseID', inplace=True)
my_listtt = df_wh["WarehouseName"].tolist()

my_r = []
for r in df_wh.index:
    my_r.append(int(r.split('-')[1]))

cols = []
rows = []

list_wh_add = []
list_count = []

tree = ET.parse(file_xml)
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
                for s in df_wh.index:
                    try:
                        zalogape = (jjj.find(s)).text

                        w = int(s.split('-')[1])
                        if zalogape != '':
                            if zalogape == '-1':
                                list_count.append(0)
                                qqq = []
                                print(len(qqq))
                            else:
                                qqq = f'"{df_wh.loc[s]["WarehouseName"]}"'
                                # print(f'{s} --> {qqq}')
                                list_wh_add.append(qqq)
                                list_count.append(zalogape)
                        else:
                            list_count.append(0)
                    except:
                        list_count.append(0)

                if len(qqq) == 0:
                    lst_txt = '""'
                    print(lst_txt)
                else:
                    #print(list_wh_add)
                    lst_txt = str(list_wh_add).replace("['", "[").replace("']", "]").replace("', '", ", ").strip()
                    #print(f'{lst_txt}\n')
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

df.to_csv(file_csv, index=False, sep=',')

def log():
    # time.sleep(1)
    finish_time = time.time() - start_time
    a = f"TIME: {finish_time}"
    cur_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    b = f"TIME_now: {cur_time}"

    log_data = []
    log_data.append(
        {
            'start_time': start_time,
            'finish_time': finish_time,
            'cur_time': b
        }
    )
    with open(file_log, 'w', encoding='utf-8') as file:
       json.dump(log_data, file, indent=4, ensure_ascii=False)


def main():
    log()


if __name__ == "__main__":
    main()
