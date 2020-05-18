# INSTALL
## Docker
Run `docker run --publish 8080:5000 --detach --name plug synbiohub/snapgene-download-plugin:snapshot` Check it is up using localhost:8080/gbAnnotate/status.

## Python
Using python run `pip install -r requirements.txt` to install the requirements.
then run `FLASK_APP=snapgene_v001_20191020 python -m flask run`.
A flask module will run at localhost:5000/gbAnnotate/.
