import json
from pathlib import Path
from urllib.request import urlopen

thu_muc = Path('du_lieu')
for ma in ['NY.GDP.MKTP.KD', 'NY.GDP.MKTP.KD.ZG']:
    url = 'https://api.worldbank.org/v2/country/VNM/indicator/' + ma
    url += '?date=2014:2023&format=json&per_page=100'
    with urlopen(url, timeout=40) as phan_hoi:
        du_lieu = json.load(phan_hoi)
    tep = thu_muc / (ma + '.json')
    tep.write_text(json.dumps(du_lieu), encoding='utf-8')
    print('Ma chi tieu:', ma)
    print('So ban ghi:', len(du_lieu[1]))
    print('Cap nhat:', du_lieu[0]['lastupdated'])
    print('Da luu:', tep)

print('Lay du lieu World Bank thanh cong.')
