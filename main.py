from automlstreams.streams import KafkaStream
from skmultiflow.evaluation import EvaluatePrequential
from automlstreams.meta import MetaClassifier
from skmultiflow.trees import HoeffdingTree

DEFAULT_BROKER = 'broker:29092'
MAX_SAMPLES = 20000


def run(topic, model=MetaClassifier(), broker=DEFAULT_BROKER):
    print(f'Running demo for topic={topic} and broker={broker}')
    stream = KafkaStream(topic, bootstrap_servers=broker)

    stream.prepare_for_use()

    model_name = model.__class__.__name__

    evaluator = EvaluatePrequential(show_plot=False,
                                    n_wait=200,
                                    batch_size=200,
                                    pretrain_size=500,
                                    max_samples=MAX_SAMPLES,
                                    output_file=f'automl-streams/results/meta.{model_name}.{topic}.csv')

    evaluator.evaluate(stream=stream, model=model)


if __name__ == "__main__":
    run('test_topic')
