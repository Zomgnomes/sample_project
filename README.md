Sample Project
==============

## To run
+ run `docker-compose up --build`

## To load example data
+ run `docker exec -it sample_project-backend-1 /bin/bash` to access the container
+ then run `python manage.py loaddata apps/data/fixtures/example_data.json.gz` to load data
+ Please note this may take a few minutes for the load to complete.
