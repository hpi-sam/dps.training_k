# Deployment Process

There are always two environment files provided with the docker-compose files in the artifacts: `.env.prod` and `.env.dev`.
The `.env.prod` file is intended for the production version on a server and the `.env.dev` file is intended for the development version locally.
Replace `<prod/dev>` with `prod` or `dev` in the following commands to use the respective environment file.

Note that the program assumes that frontend and backend are running on the same server - this is due to how nginx is configured. Other than that 
both projects should work independently.

1. Prerequisites: Install Docker and Docker Compose on the server(s) where you want to deploy the software.
2. Adjust the IP address of the server running the Frontend by changing the `CORS_ALLOWED_ORIGINS` variable within the 
   `backend/dps_training_k/configuration/settings.py` file in the backend project.
3. Adjust the IP address of the server running the Backend in the `./frontend/.env.<prod/dev>` file by setting the `VITE_SERVER_URL` variable. 
4. Trigger the `deploy` workflow in the GitHub Actions tab of the repository (note: the workflow will also be triggered automatically on each
   release). This will upload the needed images to [GitHub Packages](https://github.com/orgs/hpi-sam/packages?repo_name=dps.training_k) and save
   the needed files as [Actions Artifacts](https://github.com/hpi-sam/dps.training_k/actions/workflows/deploy.yml).
5. Download the action artifacts and extract them in a folder. Alternatively, you can manually copy the needed files from the repo (
   `./docker-compose.<dev/prod>.yml`, `./.env.<prod/dev>`, `./backend/dps_training_k/deployment/nginx/nginx_deploy_<dev/prod>.conf`).
6. Recommended: As the env files are probably stored in a public repository, it is strongly encouraged to change the `SECRET_KEY` and the
   `POSTGRES_PASSWORD` variables in the used `.env.<prod/dev>` file.
7. Log into the GitHub Packages registry with the following command. Ask a team member with access to the repository for valid credentials. Note: 
   passing secrets as command line arguments is insecure. consider using `--password-stdin` instead.
```bash
docker login ghcr.io -u <username> -p <token>
```
8. Run following commands to run the containers:
```bash
docker compose -f docker-compose.<dev/prod>.yml up
```

The application is now deployed and the website should be accessible via http (`dev`) or https (`prod`). The images will be automatically updated on each 
release and the containers restarted accordingly via [Watchtower](https://github.com/containrrr/watchtower).

Note that this also means that it is currently not possible to have multiple Frontend instances deployed that talk to different backend instances.
To achieve that, the Frontend instances each need to be manually built and deployed with the correct environment variables.

## Renewing Certificates

1. ssh into the server, e.g. `ssh manager@139.162.170.6 -i .ssh/bp_server`
2. free up port 80 by stopping website: `sudo docker-compose -f docker-compose.yml down`
3. run certbot: ` sudo certbot certonly --nginx -d klinik-dps.de -d www.klinik-dps.de`
4. kill nginx: `sudo pkill nginx` (yeah it's in a weird state at this point and needs to be killed that way, don't ask me why)
5. restart website: `sudo docker-compose -f docker-compose.yml up`

If you run into problems:

1. Check if port 80 is in use by something else: `netstat -antp`
2. Allow http in firewall if necessary: `firewall-cmd --permanent --add-service=http` and `firewall-cmd --reload`
3. Make sure nginx config is fine (should be located in `/etc/nginx/conf.d`):

```
server {
    listen 80;
    server_name klinik-dps.de www.klinik-dps.de;

    root /usr/share/nginx/html;  # Base directory for web content
    index index.html;

    location /.well-known/ {
        try_files $uri $uri/ =404;
    }
}
```
