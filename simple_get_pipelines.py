# This script will get all the pipelines Ids for circle ci in JSON format

import http.client

conn = http.client.HTTPSConnection("circleci.com")

headers = { "Circle-Token": "CCIPAT_LHELwhx9EwESPff4wH3uPi_c0c1246aa9685a065b40b0902ac8459ea9ff4d36" }

conn.request("GET", "/api/v2/pipeline?org-slug=gh/finexioinc" , headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
