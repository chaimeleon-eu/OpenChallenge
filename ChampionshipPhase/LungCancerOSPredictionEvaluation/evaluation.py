from lifelines.utils import concordance_index
from pathlib import Path
from pandas import merge, DataFrame
import json

from evalutils.io import CSVLoader

_VAL_NUMBER_CASES = 80
_TEST_NUMBER_CASES = 161

INPUT_DIRECTORY="/input"
OUTPUT_DIRECTORY="/output"
NUMBER_CASES = _TEST_NUMBER_CASES


def write_metrics(*, metrics):
    # Write a json document that is used for ranking results on the leaderboard
    with open("/output/metrics.json", "w") as f:
        f.write(json.dumps(metrics))


def main():

    path_ground_truth = Path(__file__).parent / 'ground-truth' / 'reference.csv'
    path_submission = sorted(Path(INPUT_DIRECTORY).glob('*.csv'))[0]

    file_loader = CSVLoader()
    ground_truth = DataFrame(file_loader.load(fname=path_ground_truth))
    submission = DataFrame(file_loader.load(fname=path_submission))

    if len(submission) != NUMBER_CASES:
        raise RuntimeError(f"{NUMBER_CASES} cases were expected in submission file and {len(submission)} "
                           f"were submitted")

    cases = merge(
        left=ground_truth,
        right=submission,
        indicator=True,
        how="outer",
        suffixes=("_ground_truth", "_prediction"),
        on="case"
    )

    c_index = concordance_index(cases["survival_time_months_ground_truth"],
                                cases["survival_time_months_prediction"],
                                cases["event"])

    print(c_index)

    final_metrics = dict()
    final_metrics["aggregates"] = {"c_index": c_index}

    write_metrics(metrics=final_metrics)


if __name__ == "__main__":
    main()
