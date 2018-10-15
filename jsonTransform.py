import json
from collections import OrderedDict
s = '{"dataset":{"1":{"data-source-type":"NATIVE","label":"医院列表数据","parameters":{"regionCode":490.1,"limit":2334}},"2":{"data-source-type":"NATIVE","label":"医院列表数据","parameters":{"regionCode":123,"limit":124345}}}}'


data = json.loads(s, object_pairs_hook=OrderedDict)

print(data["dataset"]["1"]["label"])