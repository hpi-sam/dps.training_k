# K-dPS
The K-dPS (the clinic variant of the dynamic patient simulation) simulation software for training medical personal on how to act during medical 
surges / during mass casualty incidents.
The Frontend website and backend server are two different projects. For setup instructions see the Readmes in the respective folders.

For a common understanding we use this 
[Code Glossary Notion page](https://k-dps.notion.site/9e82c16b6d9248679b87e0403bbf81a9?v=06e889f90e834b7baf2f879f9ad9551b&pvs=4) (note that this 
is an internal document and therefore neither formulated for others to understand nor 
written in English)

## Deployment process
The deployment process is automatically started on each release and can be manually triggered by running the GitHub action `deploy`.
This uploads the needed images to [GitHub Packages](https://github.com/orgs/hpi-sam/packages?repo_name=dps.training_k) and saves the needed 
environment variables as well as the docker-compose file as 
[Actions Artifacts](https://github.com/hpi-sam/dps.training_k/actions/workflows/deploy.yml).
For deployment, the following steps are needed:
1. Download the action artifacts and extract them in a folder
2. Pull all the docker images from GitHub Packages using `docker pull ghcr.io/hpi-sam/dps.training_k:<image-name>`
3. Additionally, pull the public redis image using `docker pull redis:latest`
4. Run the docker-compose file from step 1 using `docker-compose up`

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
