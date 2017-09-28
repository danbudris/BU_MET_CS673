# pull the image to your local machine
docker pull danbudris/bu_met_cs673

# run the container, mapping host port 8080 to container port 8000
docker run -d --name=cs673.test -p 8080:8000 danbudris/cs673:latest

# now, view the project at 127.0.0.1:8080
# or, connect to it from the command line:
docker exec -it cs673.test bash
