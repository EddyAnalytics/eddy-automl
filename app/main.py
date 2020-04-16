import sys
from automlstreams.streams import KafkaStream
from automlstreams.meta import MetaClassifier
from skmultiflow.trees import HoeffdingTree
from skmultiflow.evaluation import EvaluatePrequential
from kafka import KafkaConsumer, KafkaProducer
from io import StringIO
import pandas as pd
import numpy as np

from config import *

def run_indefinetly(input_topic, output_topic, target_index, model=HoeffdingTree()):
    print(f'Running AutoML for input_topic={input_topic}, output_topic={output_topic}, target_index={target_index} and broker={BOOTSTRAP_SERVERS}.')
    consumer = KafkaConsumer(
            input_topic,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            group_id=None,
            auto_offset_reset='earliest',
            value_deserializer=lambda x: x.decode('utf-8')
        )
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, value_serializer=lambda x: x.encode('utf-8'))

    i = 0
    total_predictions = 0
    correct_predictions = 0
    accuracy = 0

    for message in consumer:
        sample = pd.read_csv(StringIO(message.value), header=None)
        i += 1

        if any(sample.dtypes == 'object'):
            print(f'Streamed sample contains text or malformatted data.')
            continue
        
        X = sample.iloc[:,:target_index]
        y = sample.iloc[:,target_index]

        # Collect metrics
        try:
            prediction = model.predict(X)
            total_predictions += 1
            if prediction[0] == y[0]:
                correct_predictions += 1
            accuracy = correct_predictions / total_predictions
            print(f'Accuracy at sample {i}: {accuracy}')
            producer.send(output_topic + '__accuracy', str(accuracy))
            producer.send(output_topic + '__pred_count', str(total_predictions))
            producer.flush()
        except Exception:
            pass

        if y.isnull().any():
            # Predict
            try:
                y_pred = pd.DataFrame(model.predict(X))
                producer.send(output_topic, y_pred.to_csv(header=False, index=False))
                producer.flush()
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

        run_indefinetly(input_topic, output_topic, target_index)
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} input_topic output_topic target_index")


