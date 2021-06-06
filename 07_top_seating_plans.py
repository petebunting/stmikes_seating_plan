import json


with open('./seat_plan_metrics.json') as f:
    plan_info = json.load(f)
    
    out_info = dict()
    for lyr in plan_info:
        out_info[lyr] = plan_info[lyr]['seats_metric']
    
    sorted_info = sorted(out_info.items(), key=lambda x: x[1], reverse=True)
    
    i = 0
    for info in sorted_info:
        print(info[0], info[1])
        i += 1
        if i > 10:
            break