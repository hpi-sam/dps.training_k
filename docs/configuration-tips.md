# Project Configuration Tips

If you want to change the configuration of the project by e.g. updating a docker-compose or env file, you need to keep following aspects in mind:
- If you change the docker-compose file of the Backend or Frontend, you may need to also adjust the main docker-compose file in the root folder.
- The environment variables are backed in the image for the Frontend. Therefore, you need to rebuild and re-upload e.g. a new Backend IP
  address if you want to change it.
- The environment variables are loaded during the container initialization for the Backend. Therefore, you need to copy changes of the Backend env
  file to the env files in the root folder.