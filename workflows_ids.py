# This Script will first fetch the 100 pipelines ids from all projects and then iterate over all all pipeline Ids and then it will output the
# workflow Ids related to pipelines

import http.client
import json

def get_pipeline_ids():
    pipeline_ids = []
    initial_url = "/api/v2/pipeline?org-slug=gh/finexioinc"
    headers = {"Circle-Token": "CCIPAT_LHELwhx9EwESPff4wH3uPi_c0c1246aa9685a065b40b0902ac8459ea9ff4d36"}

    conn = http.client.HTTPSConnection("circleci.com")
    try:
        while True:
            conn.request("GET", initial_url, headers=headers)
            res = conn.getresponse()
            if res.status != 200:
                print(f"Error: Failed to fetch data (Status Code: {res.status})")
                return None

            data = res.read().decode("utf-8")
            json_data = json.loads(data)

            for pipeline in json_data.get("items", []):
                pipeline_id = pipeline["id"]
                pipeline_ids.append(pipeline_id)

            if len(pipeline_ids) >= 100 or "next_page_token" not in json_data:
                break

            initial_url = f"/api/v2/pipeline?org-slug=gh/finexioinc&page-token={json_data['next_page_token']}"
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

    return pipeline_ids

def get_workflow_ids(pipeline_id):
    conn = http.client.HTTPSConnection("circleci.com")
    headers = {"Circle-Token": "CCIPAT_LHELwhx9EwESPff4wH3uPi_c0c1246aa9685a065b40b0902ac8459ea9ff4d36"}
    workflow_ids = []

    try:
        conn.request("GET", f"/api/v2/pipeline/{pipeline_id}/workflow", headers=headers)
        res = conn.getresponse()
        if res.status != 200:
            print(f"Error: Failed to fetch data for pipeline {pipeline_id} (Status Code: {res.status})")
            return []

        data = res.read().decode("utf-8")
        json_data = json.loads(data)

        for item in json_data.get("items", []):
            workflow_ids.append(item["id"])
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

    return workflow_ids

if __name__ == "__main__":
    pipeline_ids = get_pipeline_ids()
    if pipeline_ids:
        print("Workflow IDs:")
        for pipeline_id in pipeline_ids:
            workflow_ids = get_workflow_ids(pipeline_id)
            if workflow_ids:
                for workflow_id in workflow_ids:
                    print(f"   {workflow_id}")
