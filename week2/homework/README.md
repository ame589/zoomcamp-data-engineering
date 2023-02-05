Exercise 1
python3 etl_web_to_gcs.py
447,770

Exercise 2
0 5 1 * *"
prefect deployment build etl_web_to_gcs.py:etl_web_to_gcs -n cron_homework --cron "0 5 1 * *"
prefect deployment apply etl_web_to_gcs-deployment.yaml

Exercise 3