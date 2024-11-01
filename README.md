# AI Tutor

This is the repository for the Generative AI Tutor pioneered at [UVU](https://www.uvu.edu/).

## Development

In order to run the project in development mode:

1. Ensure [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/install/) and the [Mongo Shell](https://www.mongodb.com/try/download/shell) are installed
2. In the project root directory, run the command `docker compose -f develop.yaml up mongo`
3. Then, run `mongosh --file ./dev/mongo-init.js`
4. In the project root directory, run the command `docker compose -f develop.yaml up --watch`
5. Everything should be up and running 😄

# Acknowledgments

- [**Dr. Ahmed Alsharif**](https://www.uvu.edu/directory/employee/?id=eXpuVHFkeWcrVkF0N2pvTjdpNmg2dz09): For making everything possible and supporting this project so wholeheartedly.
- [**Dr. Armen Ilikchyan**](https://www.uvu.edu/directory/employee/?id=ZnBHYXBLNUN3cUgvV2ZNQjFVTEUzdz09): For paving the way, and providing invaluable guidance.
