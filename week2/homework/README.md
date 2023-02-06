# Homework week 2


This repository contains a docker-compose.yml file for setting up a multi-container application.
Prerequisites

    Docker
    Python
    Prefect

Usage

    Clone this repository to your local machine:

git clone [https://github.com/ame589/homework_week_1.git](https://github.com/ame589/homework_week_1.git)

    Navigate to the repository directory:

Exercises solutions:

## Exercise n.1

1. python3 etl_web_to_gcs.py

## Exercise n.2

1. prefect deployment build etl_web_to_gcs.py:etl_web_to_gcs -n cron_homework --cron "0 5 1 * *"
2. prefect deployment apply etl_web_to_gcs-deployment.yaml

## Exercise n.3
