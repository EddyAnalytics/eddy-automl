FROM confluentinc/cp-kafkacat:latest

COPY _datasets .

ENTRYPOINT [ "./_publish_to_kafka.sh" ]