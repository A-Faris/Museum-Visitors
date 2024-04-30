# Pipeline

This folder should contain all code, documentation and resources required for the pipeline.

- 'extract.py' - An extract Python script that connects to S3 and downloads files relevant to the project

- 'schema.sql' - A database setup script that creates required database tables and seeds them with initial data

- 'pipline.py' - A pipeline script that downloads kiosk data from S3 and uploads it to the database

- 'analysis.ipynb' - An analysis notebook, that connects to the database and explores the data it contains