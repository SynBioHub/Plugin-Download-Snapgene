# INSTALL
## Docker
Run `docker run --publish 8080:5000 --detach --name snapgene-download-plug synbiohub/plugin-download-snapgene:snapshot` Check it is up using localhost:8080/plain/png/status. 

## Python
Using python run `pip install -r requirements.txt` to install the requirements.
then run `FLASK_APP=app.py python -m flask run`.
A flask module will run at localhost:5000/annotate/zip/run.
