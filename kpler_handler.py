from kpler.sdk.configuration import Configuration
from kpler.sdk import Platform,FlowsDirection, FlowsSplit, FlowsPeriod, FlowsMeasurementUnit,RefinedProducts
from kpler.sdk.resources.flows import Flows
from datetime import date
import utility_dicts as ud
import json
fl=open('conf.json')
crd=json.load(fl)
usr=crd['username']
psw=crd['password']
conf=Configuration(Platform.Liquids,usr,psw)


# available platforms Liquids and LNG
# info on ships and ports
#
def request_handler():
    pass

def flow_handler(arg_dict,conf):
    fl=Flows(conf)

    #although it's bad practice to do more than one thing at value asignment, in this case it is meant simply to not write redundant lines
    #the only thing being done is using the dictionaries stored on utility dicts to output the correct objects that will be passed onto kpler
    flow_dir=ud.flow_dir[arg_dict['dataset']]
    from_zone=arg_dict['countries']
    start=arg_dict['start_date']
    end=arg_dict['end_date']
    unit=ud.flow_units[arg_dict['units']]
    period=ud.flow_period[arg_dict['period']]
    split=ud.flow_split[arg_dict['split']]
    product=arg_dict['product']
    
    data=fl.get(flow_direction=[flow_dir],
           split=[split],
           granularity=[period],
           start_date=start,
           end_date=end,
           unit=[unit],
           products=product,
           from_zones=from_zone)
    return data