# AI Tutor

This is the repository for the Generative AI Tutor pioneered at [UVU](https://www.uvu.edu/).


![AI Tutor Homepage](./assets/mainpage.png)

## Introduction

The AI Tutor project has been under active development for quite some time, started back in early 2024.
In discussions with the excellent faculty in the Tech Management Department at Utah Valley University,
we hypothesized that using the new and exciting technology of large language models,
we could provide excellent, _personalized_ tutoring to students *whenever they needed it*.

So, we set out to provide a novel way to accomplish this goal.
The original AI Tutor was indeed a success, quickly being adopted into a several courses at Utah Valley University,
and gaining attention among multiple departments and more than a handful of students.

This repository is where that code lives.


## Design

![An overview of the system design of the AI Tutor](./assets/ai-tutor-2-diagram-light.png)

## Development

In order to run the project in development mode:

1. Ensure [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed.
2. In the project root directory, run the command: `docker compose -f develop.yaml build`
3. Then, still in the project root, run: `docker compose -f develop.yaml up --watch`
4. Everything should be up and running 😄

![Docker Building](./assets/compiling.png)
![Docker Running](./assets/dockerrunning.png)

## Deployment

- Our deployments are hosted on a [Hetzner](https://www.hetzner.com/cloud) virtual private server.

1. We use [just](https://github.com/casey/just) to bundle everything needed to deploy into one command `just deploy`
2. This essentially just uses `rsync` and `ssh` to send the files up, build the docker containers, and run them.



# Acknowledgments

- [**Dr. Ahmed Alsharif**](https://www.uvu.edu/directory/employee/?id=eXpuVHFkeWcrVkF0N2pvTjdpNmg2dz09): For making everything possible and supporting this project so wholeheartedly.
- [**Dr. Armen Ilikchyan**](https://www.uvu.edu/directory/employee/?id=ZnBHYXBLNUN3cUgvV2ZNQjFVTEUzdz09): For paving the way, and providing invaluable guidance.
