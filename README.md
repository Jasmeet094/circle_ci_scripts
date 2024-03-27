# circle_ci_scripts


1. get_failed_jobs.py - This script is to get the failed jobs along with job's related workflow and id. (Export API_TOKEN env var before running)

2. get_failed_jobs_lambda - AWS Lambda code to get the failed jobs from circle ci all projects. (In configuration add API_TOKEN env var)

3. pipeline_ids.py  - To get first 100 pipelines Ids

4. simple_get_pipelines.py - simple python script to get the all pipelines details as JSON format

5. workflows_ids.py  -  to get the workflow IDs , it will automatiically get the pipelines ids and then iterate over the pipelines ids to get the workflow ids.
   
