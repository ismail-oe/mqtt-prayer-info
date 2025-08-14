import json, os
from datetime import datetime
import paho.mqtt.client as mqtt
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
timestamp = datetime.now().isoformat()

# load .json file with prayer times
def load_config(path=os.path.join(script_dir, "config.json")):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

# load config.json
config = load_config()

# return array with yesterday, today and tomorrow prayer times
def getTime(json_path):
    index = datetime.today().timetuple().tm_yday - 1

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    try:
        return [data["data"][index], data["data"][index+1]]
    except IndexError:
        return None

data_path = os.path.join(script_dir, config["data_path"])

data_today = getTime(data_path)[0]
data_tomorrow = getTime(data_path)[1]

if data_today and data_tomorrow:
    client = mqtt.Client()
    client.connect(config["mqtt_host"], config["mqtt_port"], 60)

    client.publish(config["mqtt_publish_path"] + "/today", json.dumps(data_today), retain=True)
    client.publish(config["mqtt_publish_path"] + "/tomorrow", json.dumps(data_tomorrow), retain=True)

    client.disconnect()

else:
    print("No prayer-times found.")