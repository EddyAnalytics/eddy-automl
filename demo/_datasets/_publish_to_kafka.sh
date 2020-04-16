#!/bin/bash
if [[ -z "$KAFKA_BROKER" ]]; then
    echo "KAFKA_BROKER is unset or set to the empty string. Using localhost"
fi

until kafkacat -b ${KAFKA_BROKER:-localhost} -L; do
  sleep 5
done

for file in *.csv; do
    echo "Publishing to ${KAFKA_BROKER:-localhost}"
    cat $file | kafkacat -P -b ${KAFKA_BROKER:-localhost} -t ${file%.*}
    echo "Published $file to ${file%.*}"
done