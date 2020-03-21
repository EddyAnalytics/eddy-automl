import sys
import pandas as pd


def run(filename):
    df = pd.read_csv(f'_datasets/{filename}.csv', comment='#')
    y = df[['class']]
    X = df.drop(columns=['class'])
    df = pd.concat([X, y], axis=1)
    df.to_csv(f'_datasets/{filename}.csv', index=None)


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} filename")
    run(filename)
