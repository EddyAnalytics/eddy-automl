import sys
from automlstreams.meta import LastBestClassifier
from skmultiflow.evaluation import EvaluatePrequential
from kafka import KafkaConsumer, KafkaProducer
from io import StringIO
import pandas as pd
import numpy as np

from random import random

from skmultiflow.trees import HoeffdingTree

DEFAULT_BROKER = 'localhost:9092'

def run_indefinetly(input_topic, output_topic, target_index, broker=DEFAULT_BROKER, model=HoeffdingTree()):
    print(f'Running AutoML for input_topic={input_topic}, output_topic={output_topic} and broker={broker}')
    consumer = KafkaConsumer(
            input_topic,
            bootstrap_servers=broker,
            group_id=None,
            auto_offset_reset='earliest',
            value_deserializer=lambda x: x.decode('utf-8')
        )
    producer = KafkaProducer(value_serializer=lambda x: x.encode('utf-8'))

    total_predictions = 0
    correct_predictions = 0
    accuracy = 0

    for message in consumer:
        sample = pd.read_csv(StringIO(message.value), header=None)

        if any(sample.dtypes == 'object'):
            print(f'Streamed sample contains text or malformatted data.')
            continue
    
        X = sample.iloc[:,:target_index]
        y = sample.iloc[:,target_index]

        if y.isnull().any():
            # Predict
            try:
                y_pred = pd.DataFrame(model.predict(X))
                producer.send(output_topic, y_pred.to_csv(header=False, index=False))
            except Exception as e:
                print('An exception occured during prediction', e)
        else:
            # Train
            try:
                model.partial_fit(X, y)
            except Exception as e:
                print('An exception occured during training', e)


if __name__ == "__main__":
    try:
        input_topic = sys.argv[1]
        output_topic = sys.argv[2]
        target_index = int(sys.argv[3])
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} input_topic output_topic target_index")

    run_indefinetly(input_topic, output_topic, target_index)
