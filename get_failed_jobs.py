# This script outputs the failed jobs for a workflow. It will show the workflow id and jobs ids which are 
# failed in a specific workflow




import http.client
import json
import os

def get_pipeline_ids():
    pipeline_ids = []
    initial_url = "/api/v2/pipeline?org-slug=gh/finexioinc"
    headers = {"Circle-Token": os.getenv("API_TOKEN")}  # Using environment variable

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
    headers = {"Circle-Token": os.getenv("API_TOKEN")}  # Using environment variable
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

def get_job_details(workflow_id):
    conn = http.client.HTTPSConnection("circleci.com")
    headers = {"Circle-Token": os.getenv("API_TOKEN")}  # Using environment variable
    job_details = []

    try:
        conn.request("GET", f"/api/v2/workflow/{workflow_id}/job", headers=headers)
        res = conn.getresponse()
        if res.status != 200:
            print(f"Error: Failed to fetch job details for workflow {workflow_id} (Status Code: {res.status})")
            return []

        data = res.read().decode("utf-8")
        json_data = json.loads(data)

        for item in json_data.get("items", []):
            job_details.append(item)
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

    return job_details

if __name__ == "__main__":
    pipeline_ids = get_pipeline_ids()
    if pipeline_ids:
        counter = 1
        for pipeline_id in pipeline_ids:
            workflow_ids = get_workflow_ids(pipeline_id)
            if workflow_ids:
                for workflow_id in workflow_ids:
                    failed_jobs = []
                    job_details = get_job_details(workflow_id)
                    if job_details:
                        for job_detail in job_details:
                            if job_detail['status'] == 'failed':
                                failed_jobs.append({'id': job_detail['id'], 'job_number': job_detail['job_number'], 'status': job_detail['status']})

                    if failed_jobs:
                        print(f"{counter}. Workflow ID: {workflow_id}")
                        print("      'project_slug': 'gh/finexioinc/fx-ng'")
                        for job in failed_jobs:
                            print(f"      'id': '{job['id']}',")
                            print(f"      '{job['job_number']}': {job['status']}")
                        print("\n")
                        counter += 1
