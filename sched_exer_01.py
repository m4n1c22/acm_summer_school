import json
from urllib.request import urlopen
import requests
response = urlopen("http://localhost:5000/redfish/v1/CompositionService/ResourceBlocks")
json_data = json.loads(response.read().decode('utf-8'))

resource_blocks_numbers= json_data["Links"]["Members@odata.count"]

blocks = json_data["Links"]["Members"]
print("Available resource blocks : "+str(resource_blocks_available))
processor_blocks =[]
sas_blocks =[]
for block in blocks:
    dict_block = {}
    url_block = block["@odata.id"]
    response = urlopen("http://localhost:5000"+str(url_block))
    json_data = json.loads(response.read().decode('utf-8'))
    #print (json_data)
    processors_count = len(json_data["Processors"])
    sas_count = len(json_data["SimpleStorage"])
    #print (processors_count)
    #print (sas_count)
    if processors_count>0:
        dict_block = {"count":processors_count,"block_url":url_block}
        processor_blocks.append(dict_block)
    if sas_count>0:
        dict_block = {"count":sas_count,"block_url":url_block}
        sas_blocks.append(dict_block)

#available blocks:

print ("available processor blocks")
for block in processor_blocks:
    print (block)
print ("available sas blocks")
for block in sas_blocks:
    print (block)

required_sas = 4
required_procs = 4

request_blocks= []

for block in processor_blocks:
    dict_int_block = {}
    if required_procs > block["count"]:
        required_procs = required_procs - block["count"]
        dict_int_block = {"@odata.id":block["block_url"]}
        request_blocks.append(dict_int_block)
    else:
        dict_int_block = {"@odata.id":block["block_url"]}
        request_blocks.append(dict_int_block)
        required_procs = 0
    if required_procs == 0:
        break

for block in sas_blocks:
    dict_int_block = {}
    if required_sas > block["count"]:
        required_sas = required_sas - block["count"]
        dict_int_block = {"@odata.id":block["block_url"]}
        request_blocks.append(dict_int_block)
    else:
        dict_int_block = {"@odata.id":block["block_url"]}
        request_blocks.append(dict_int_block)
        required_sas = 0
    if required_sas == 0:
        break
 
#request blocks
print (request_blocks)

request_new_comp = {"Name": "Assignment01","Links":{"ResourceBlocks":request_blocks}}        
json_request = json.dumps(request_new_comp)

#create composition
r=requests.post("http://localhost:5000/redfish/v1/Systems",json_request)
print ("Added a composition "+ r.text)
#delete composition
r=requests.delete("http://localhost:5000/redfish/v1/Systems/Assignment01")
print ("Deleted a composition "+r.text)
