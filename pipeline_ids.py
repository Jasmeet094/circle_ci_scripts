import http.client
import json

# Define the initial request URL and headers
initial_url = "/api/v2/pipeline?org-slug=gh/finexioinc"
headers = {"Circle-Token": "CCIPAT_LHELwhx9EwESPff4wH3uPi_c0c1246aa9685a065b40b0902ac8459ea9ff4d36"}

# Perform the initial request
conn = http.client.HTTPSConnection("circleci.com")
conn.request("GET", initial_url, headers=headers)
res = conn.getresponse()
data = res.read().decode("utf-8")

# Load the JSON response
json_data = json.loads(data)

# Extract pipeline IDs and print them in the desired format
pipeline_ids = []
page = 1

while True:
    for pipeline in json_data["items"]:
        pipeline_ids.append(pipeline["id"])
        print(f"{len(pipeline_ids)}. Pipeline {pipeline['id']}")
        if len(pipeline_ids) == 100:
            break

    if len(pipeline_ids) == 100 or "next_page_token" not in json_data:
        break

    # Get the next page using the token
    next_page_token = json_data["next_page_token"]
    conn.request("GET", f"{initial_url}&page-token={next_page_token}", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    json_data = json.loads(data)

# Close the connection
conn.close()
