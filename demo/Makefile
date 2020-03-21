# Start all services: Eddy AutoML + Kafka Cluster
up:
	docker-compose up

# Stop and remove all containers
down:
	docker-compose down

# Publish the files from the _datasets folder to Kafka using kafkacat
publish-datasets:
	cd ./_datasets && ./_publish_to_kafka.sh