# Eddy AutoML 

AutoML component for streaming data

## Development

Start the Docker compose services: 
```bash
docker-compose up
```

A Kafka broker will be exposed at `localhost:9092` locally and at `broker:29092` in the bridge network created by Docker compose.

Run the `main.py` file:

```bash
docker-compose exec eddy-automl python main.py in_topic out_topic target_column_index
```

Example:
```bash
docker-compose exec eddy-automl python main.py elec test 6
```