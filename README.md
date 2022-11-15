# 2022 Huawei Cloud Competition - Despro - Desire Process

<p align="center">
  <img src="https://github.com/teOrienta/2022-Huawei-cloud/blob/main/frontend/src/assets/despro_logo1.png" />
</p>

## Overview 

<p align="center">
  <img src="https://i.ibb.co/x5MfpL1/Gif-Demo.gif" />
</p>


We developed DesPro, a tool aiming to load process information automatically and display new developments through a graph system. The information is stored in the database for future analysis. After loading the data, the discovered processes are displayed in an interactive and intuitive manner, allowing specialists and officials to easily analyze the graph in search of possible bottlenecks and deviations from the desired processes. To further enhance user analysis, DesPro counts with filtering options, allowing users to restrict the pool of data being analyzed by factors such as date intervals or other criteria.

## Data source 📊

These links are the data source of the project.
- [Licitações](https://transparencia.gov.br/download-de-dados/licitacoes)
- [Dicionário](https://www.portaldatransparencia.gov.br/pagina-interna/603389-dicionario-de-dados-licitacoes)

## Get started

1. Before start you need to build the images with the following command:

```bash
docker-compose build
```

2. Then you can start the containers with the following command:

```bash
docker-compose up # or docker-compose up --force-recreate
```

### Run the Front End

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 14.0.0.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

