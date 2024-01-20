from pathlib import Path
from pandas import merge, DataFrame
import json
from sklearn import metrics
import numpy as np

from evalutils.io import CSVLoader

_VAL_NUMBER_CASES = 59
_TEST_NUMBER_CASES = 118

INPUT_DIRECTORY="/input"
OUTPUT_DIRECTORY="/output"
NUMBER_CASES = _TEST_NUMBER_CASES


def micro_specificity_calculation(y_true, y_pred, classes):
    TN_total = 0
    FP_total = 0

    for c in classes:
        # Consider the actual class as positive and the remaining classes as negative
        y_true_class = (y_true == c)
        y_pred_class = (y_pred == c)

        # Calculate confusion matrix
        tn, fp, fn, tp = metrics.confusion_matrix(y_true_class, y_pred_class).ravel()

        # Accumulate true negatives and false positives
        TN_total += tn
        FP_total += fp

    # Calculate micro-averaged specificity
    specificity_micro = TN_total / (TN_total + FP_total)
    return specificity_micro


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

    y_test = cases["histology_subtype_ground_truth"]
    y_pred_prob_other = cases["other_prob"]
    y_pred_prob_dcis = cases["dcis_prob"]
    y_pred_prob_idc = cases["idc_prob"]
    y_pred_prob_ilc = cases["ilc_prob"]

    y_pred_prob = np.column_stack((y_pred_prob_other, y_pred_prob_dcis, y_pred_prob_idc, y_pred_prob_ilc))

    auc = metrics.roc_auc_score(y_test, y_pred_prob, multi_class='ovr')

    micro_sensitivity = metrics.recall_score(cases["histology_subtype_ground_truth"],
                                             cases["histology_subtype_prediction"],
                                             average='micro')

    micro_specificity = micro_specificity_calculation(cases["histology_subtype_ground_truth"],
                                                      cases["histology_subtype_prediction"],
                                                      classes=[0, 1, 2, 3])

    balanced_accuracy = metrics.balanced_accuracy_score(cases["histology_subtype_ground_truth"],
                                                        cases["histology_subtype_prediction"])

    score = 0.4 * auc + 0.2 * micro_sensitivity + 0.2 * micro_specificity + 0.2 * balanced_accuracy

    final_metrics = dict()
    final_metrics["aggregates"] = {
            "auc": auc,
            "micro_sensitivity": micro_sensitivity,
            "micro_specificity": micro_specificity,
            "balanced_accuracy": balanced_accuracy,
            "score": score
        }

    write_metrics(metrics=final_metrics)


if __name__ == "__main__":
    main()
