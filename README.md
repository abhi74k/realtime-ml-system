## Overview

This project is a realtime ML system that will predict short term crypto price movements. 


## Motivation

I have been working with ML models for a while now and I have a reasonably good understanding of the inner workings of models and pipelines. 
This project is an attempt to build an end to end ML system. How do I turn an ML model into a product? How do I deploy it? How do I monitor it? How do I scale it?

## Technologies

- RedPanda : Messaging System (Kafka alternative/compatible)
- QuixStreams : Stream processing library
- Kraken : Crypto market data provider
- Websocket-client : Websocket client library (Connection to Kraken API)
- Docker & Docker Compose : Containerization
- Loguru : Logging
- Poetry : Dependency Management

## Getting Started

### RedPanda

Go to the `docker-compose` directory and run the following commands

| Command                        | Description                    |
|-------------------------------|--------------------------------|
| `make start`                  | Starting RedPanda              |
| `make stop`                   | Stopping RedPanda              |


### Trade Producer

Go to the `services/trade_producer` directory and run the following commands

| Command                       | Description                    |
|-------------------------------|--------------------------------|
| `make build`                  | Building the docker image      |
| `make run`                    | Running the docker container   |
| `make stop`                   | Stopping the docker container  |
| `make clean`                  | Cleaning up the docker container|
