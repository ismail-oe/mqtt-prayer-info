import json
from datetime import datetime

def getTime(json_path):
    index = datetime.today().timetuple().tm_yday - 1

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    try:
        return data["data"][index]
    except IndexError:
        return None
    
times = getTime('raspi/ressources/times_dortmund.json')
if times:
    print("Gebetszeiten für heute:")
    for key, value in times.items():
        if key not in ["bolge_id", "tarih"] and value:
            print(f"{key}: {value}")
else:
    print("Keine Gebetszeiten für heute gefunden.")