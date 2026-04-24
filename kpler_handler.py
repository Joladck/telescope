from kpler.sdk.configuration import Configuration
from kpler.sdk import Platform,FlowsDirection, FlowsSplit, FlowsPeriod, FlowsMeasurementUnit,RefinedProducts
from kpler.sdk.resources.flows import Flows
from datetime import date
import json
fl=open('conf.json')
crd=json.load(fl)
usr=crd['username']
psw=crd['password']
conf=Configuration(Platform.Liquids,usr,psw)
fl=Flows(conf)

# available platforms Liquids and LNG
# info on ships and ports
#
def request_handler():
    pass

def flow_handler(arg_dict):
    pass