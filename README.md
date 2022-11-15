# 2022 Huawei Cloud Competition - Despro - Desire Process

<p align="center">
  <img src="https://github.com/teOrienta/2022-Huawei-cloud/blob/main/frontend/src/assets/logo-cinza.png" />
</p>

<p align = "center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/rabbitmq-%23FF6600.svg?&style=for-the-badge&logo=rabbitmq&logoColor=white"/>
</p>

## Overview 

<p align="center">
  <img src="https://i.ibb.co/x5MfpL1/Gif-Demo.gif" />
</p>


DesPro is a tool aiming to load process information automatically and display new developments through a graph system. The information is stored in the database for future analysis. After loading the data, the discovered processes are displayed in an interactive and intuitive manner, allowing specialists and officials to easily analyze the graph in search of possible bottlenecks and deviations from the desired processes. To further enhance user analysis, DesPro counts with filtering options, allowing users to restrict the pool of data being analyzed by factors such as date intervals or other criteria.

## Data source 📊

These are some of the data source of the project.
- [Licitações](https://transparencia.gov.br/download-de-dados/licitacoes)
- [Dicionário](https://www.portaldatransparencia.gov.br/pagina-interna/603389-dicionario-de-dados-licitacoes)

## Technical Architecture

Real-time process mining in which data is either streamed via messaging system or uploaded through a .CSV file, and then processed to generate intuitive and human-friendly graphs. All the heavy lifting of the application is done in the cloud.

<p align="center">
  <img src="https://i.ibb.co/5vtw56B/arqui.png" />
</p>

The following tools were chosen based on member experience and market adoption:

* FastAPI: Used to create a rest-based API in Python 3, that serves as our backend;
* Docker: Used for creation and administration of application modules.
* Angular: Used to create a responsive and expandable user interface;
* Nginx: Used to create a web server and a reverse proxy;
* PM4PY: Python library responsible for handling the algorithms and functions involved in process mining;
* PostgreSQL 13: SGBD used to store all data that is consumed by our tool;
* RabbitMQ: Messaging service used to stream new event data into our tool.


## Cloud Services Description

These were the services provided by Huawei that were used to deploy the solution:
 
* A message is sent to Rabbitmq service, hosted under Huawei’s Distributed Message Service (for RabbitMQ) containing new entries to the database;
* The new data is stored into Huawei’s RDS, specifically into a postgreSQL instance;
* The backend application, which is hosted under Huawei’s ECS compute container, is responsible for querying the database and handling end-point requests. It serves our frontend application with the process flow graphs;
* The Web app is hosted on the same instance as the backend and requests flow graphs from the it. This request can have various filter parameters to improve process analysis.
* There’s an Elastic Load Balancer set to replicate the ECS instance when CPU usage is above a certain threshold, up to a maximum of 5 copies. When the CPU usage falls below another, lower, threshold, the instances are culled.


## Get started

1. Before starting you need to build the images with the following command:

```bash
docker-compose build
```

2. Then you can start the containers with the following command:

```bash
docker-compose up # or docker-compose up --force-recreate
```

## Run the Front End

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 14.0.0.

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

