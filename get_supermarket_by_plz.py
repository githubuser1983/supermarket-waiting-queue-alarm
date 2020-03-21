from osmapi import OsmApi
lv_lidl = 218587077

MyApi = OsmApi()
print(MyApi.NodeGet(123))

lref_lidl = MyApi.NodeGet(218587077)
print(lref_lidl)