Setup:

Clone repo into desired location. Im using my home directory in this example.

Change directories into the portfolio_manager directory
`cd .~/portfolio-manager`

First build the image
 `docker build portfolio-manager .`

Then create a container
`docker run -it --name portfolio-manager -p 80:80 -v $(pwd)/app:/app portfolio-manager bash`

This command will dump you into an interactive prompt on the container and also maps the app directory into the containers working app directory to automatically sync changes for development work.
Port 80 of your system will also be mapped to port 80 if the container.

You will then be able to use a web browser and go to http://localhost