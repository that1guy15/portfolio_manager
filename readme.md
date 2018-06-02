Portfolio Manager is basic crypto currency portfolio tool used to keep track of any number of crypto coins. You can also
add transactional data of purchases into your portfolio to track performance of your coins. 

![Portfolio_Manager](portfolio_mngr.png?raw=true "Portfolio Manager")

# TODOs:
* Remove crypto from watchlist via UI
* Remove/Change transactions via UI
* Add stock market portfolio/watchlist
* More tests




# Setup:

* NOTE: I have only ran and tested this on Mac.
 
Clone repo into desired location. Im using my home directory in this example.

Change directories into the portfolio_manager directory

`cd .~/portfolio-manager`

First build the image

 `docker build -t portfolio-manager .`

Then create a container

`docker run -it --name portfolio-manager -p 80:80 -v $(pwd)/app:/app portfolio-manager bash`

This command will dump you into an interactive prompt on the container and also maps the app directory into the containers working app directory to automatically sync changes for development work.
Port 80 of your system will also be mapped to port 80 if the container.

Within the container you now need to start flask

`export FLASK_APP=main.py`

`flask run --host=0.0.0.0 --port=80`

You will then be able to use a web browser and go to http://localhost

Alternativley you can use `docker-compose up` from the project directory. 

