# K-dPS
The K-dPS (the clinic variant of the dynamic patient simulation) simulation software for training medical personnel on how to act during medical 
surges / during mass casualty incidents.
The Frontend website and backend server are two different projects. For setup instructions see the Readmes in the respective folders.

For a common understanding we use this 
[Code Glossary Notion page](https://k-dps.notion.site/9e82c16b6d9248679b87e0403bbf81a9?v=06e889f90e834b7baf2f879f9ad9551b&pvs=4) (note that this 
is an internal document and therefore neither formulated for others to understand nor 
written in English)

## Deployment process
The described deployment process here is for setting up the frontend and backend at the same time via docker. If you want to deploy just one via 
docker or want to run the frontend without docker, please refer to the respective Readmes in the frontend and backend folders.

The deployment process is automatically started on each release and can be manually triggered by running the GitHub action `deploy`.
This uploads the needed images to [GitHub Packages](https://github.com/orgs/hpi-sam/packages?repo_name=dps.training_k) and saves the needed 
environment variables as well as the docker-compose file as 
[Actions Artifacts](https://github.com/hpi-sam/dps.training_k/actions/workflows/deploy.yml).
There are two environment files provided with the docker-compose file in the artifacts: `.env.prod` and `.env.dev`.
The `.env.prod` file is used for the production version on a server and the `.env.dev` file is used for the development version locally.
Replace `<prod/dev>` with `prod` or `dev` in the following commands to use the respective environment file.
0. Prerequisites: Install Docker and Docker Compose on the server where you want to deploy the software.
1. Download the action artifacts and extract them in a folder. Alternatively, you can manually copy the needed files from the repo (.
   /docker-compose.yml, ./.env.<prod/dev>).
2. Recommended: As the env files are probably stored in a public repository, it is strongly encouraged to change the SECRET_KEY and the 
   POSTGRES_PASSWORD variables in the used `.env.<prod/dev>` file.
3. Log into the GitHub Packages registry with the following command. Ask a team member for valid credentials. Note: passing secrets as 
   command line arguments is insecure. consider using `--password-stdin` instead
```bash
docker login ghcr.io -u <username> -p <token>
```
4. Optional: If you want a clean start and have the application already running, execute following command in that folder in order to recreate the 
   database:
```bash
docker-compose --env-file .env.<prod/dev> down --volumes
```
5. Run following commands to pull the newest images (only needed if already setup once) and build and run the containers:
```bash
docker-compose --env-file .env.<prod/dev> pull
docker-compose --env-file .env.<prod/dev> up
```

The application is now deployed and the website should be accessible on port 5173. The images will be automatically updated on each release and 
the containers restarted accordingly.

Keep in mind that the IP address of the server running the back- and frontend are hardcoded in the environment files. For 
the backend a simple correction of the `CORS_ALLOWED_ORIGINS` variable within the `backend/dps_training_k/configuration/settings.py` file on the 
server is enough, but for the frontend the `VITE_SERVER_URL` variable has to be adjusted in the associated env file and the image has 
to be rebuilt and re-uploaded to the GitHub Packages registry.

## Changing the project configuration
If you want to change the configuration of the project by e.g. updating a docker-compose or env file, you need to keep following aspects in mind:
- If you change the docker-compose file of the backend or frontend, you may need to also adjust the main docker-composer file in the root folder.
- The environment variables are backed in the image for the Frontend. Meaning you need to rebuild and re-upload e.g. a new Backend IP Address if you 
  want to change it.
- The environment variables are loaded during the container initialization for the backend. Therefore, you need to copy changes of the backend env 
  file to the env files in the root folder.

## MoSCoW and future plans
We follow this [MoSCoW Notion page](https://k-dps.notion.site/MoSCoW-78d8a9b852f7499bb7fb47a770c30723?pvs=4) (note that this is an internal 
document and therefore neither formulated for others to understand nor written in English)

In addition to that we aim to always incorporate following non-functional requirements into our development:

### Non-functional Requirements 
- A00: Customizability
  - Our software allows for high customizability before and during the exercise. This recognizes the educational key role of exercise instructors.
- A01: Intuitive Interface
  - The interface is intuitive for hospital staff.
- A02: Easy Simulation Execution
  - The simulation should be quick to prepare and execute.
- A03: 8-25 Participants
  - The exercises are effectively playable by 8-25 participants.
- A04: Screen Ratio 3:4 to 1:2
  - The web app should correctly scale on all screen ratios from 3:4 to 1:2.
- A05: Samsung S7 FE
  - The web app should look good on the Samsung S7 FE.
- A06: Chrome, Firefox, and Safari
  - The web app should work on the latest versions of Chrome, Firefox, and Safari.
- A07: Backend Performance
  - A backend should be able to handle a single exercise with 30 clients.
 
## Interface Definition
The communication between the frontend and backend uses an Interface as defined in our
[interface definition Notion page](https://k-dps.notion.site/Interface-Definition-6852697ae02f41b29544550f84e1049a)(note that this is an internal 
document and therefore not necessarily formulated for others to understand)
