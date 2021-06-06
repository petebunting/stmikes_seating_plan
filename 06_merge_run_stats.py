import glob
import json

def readJSON2Dict(input_file):
    with open(input_file) as f:
        data = json.load(f)
    return data

json_files = glob.glob('./out_plans/*.json')


out_metrics = dict()

for json_file in json_files:
    json_data = readJSON2Dict(json_file)
    
    for lyr in json_data:
        out_metrics[lyr] = json_data[lyr]

with open('./seat_plan_metrics.json', 'w') as fp:
    json.dump(out_metrics, fp, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

    

