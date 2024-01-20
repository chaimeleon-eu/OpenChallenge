from pathlib import Path
from pandas import merge, DataFrame
import json
from sklearn import metrics
import numpy as np
import math

from evalutils.io import CSVLoader

_VAL_NUMBER_CASES = 55
_TEST_NUMBER_CASES = 105

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

    # Tumor pathological category (T)
    y_test = cases["t_ground_truth"]
    y_pred_prob_t1_t2 = cases["t1_t2_prob"]
    y_pred_prob_t3 = cases["t3_prob"]
    y_pred_prob_t4a = cases["t4a_prob"]
    y_pred_prob_t4b = cases["t4b_prob"]

    y_pred_prob = np.column_stack((y_pred_prob_t1_t2, y_pred_prob_t3, y_pred_prob_t4a, y_pred_prob_t4b))

    auc_t = metrics.roc_auc_score(y_test, y_pred_prob, multi_class='ovr')

    micro_sensitivity_t = metrics.recall_score(cases["t_ground_truth"],
                                               cases["t_prediction"],
                                               average='micro')

    micro_specificity_t = micro_specificity_calculation(cases["t_ground_truth"],
                                                        cases["t_prediction"],
                                                        classes=[0, 1, 2, 3])

    balanced_accuracy_t = metrics.balanced_accuracy_score(cases["t_ground_truth"],
                                                          cases["t_prediction"])

    score_t = 0.4 * auc_t + 0.2 * micro_sensitivity_t + 0.2 * micro_specificity_t + 0.2 * balanced_accuracy_t

    # Regional nodes pathological category (N)
    y_test = cases["n_ground_truth"]
    y_pred_prob_n0 = cases["n0_prob"]
    y_pred_prob_n1 = cases["n1_prob"]
    y_pred_prob_n2 = cases["n2_prob"]

    y_pred_prob = np.column_stack(
        (y_pred_prob_n0, y_pred_prob_n1, y_pred_prob_n2))

    auc_n = metrics.roc_auc_score(y_test, y_pred_prob, multi_class='ovr')

    micro_sensitivity_n = metrics.recall_score(cases["n_ground_truth"],
                                               cases["n_prediction"],
                                               average='micro')

    micro_specificity_n = micro_specificity_calculation(cases["n_ground_truth"],
                                                        cases["n_prediction"],
                                                        classes=[0, 1, 2])

    balanced_accuracy_n = metrics.balanced_accuracy_score(cases["n_ground_truth"],
                                                          cases["n_prediction"])

    score_n = 0.4 * auc_n + 0.2 * micro_sensitivity_n + 0.2 * micro_specificity_n + 0.2 * balanced_accuracy_n

    # Metastasis pathological category (M)

    fpr, tpr, _ = metrics.roc_curve(cases["m_ground_truth"], cases["m1_prob"],
                                    pos_label=1)  # positive class is 1; negative class is 0
    auc_m = metrics.auc(fpr, tpr)
    if math.isnan(auc_m):
        auc_m = 0
    balanced_accuracy_m = metrics.balanced_accuracy_score(cases["m_ground_truth"],
                                                          cases["m_prediction"])
    f1_score_m = metrics.f1_score(cases["m_ground_truth"], cases["m_prediction"])
    sensitivity_m = metrics.recall_score(cases["m_ground_truth"], cases["m_prediction"])
    tn, fp, fn, tp = metrics.confusion_matrix(cases["m_ground_truth"],
                                              cases["m_prediction"]).ravel()
    specificity_m = tn / (tn + fp)
    score_m = 0.4 * auc_m + 0.2 * sensitivity_m + 0.2 * specificity_m + 0.2 * balanced_accuracy_m

    # Final score
    score = 0.4 * score_t + 0.3 * score_n + 0.3 * score_m

    final_metrics = dict()
    final_metrics["aggregates"] = {
            "score_t": score_t,
            "auc_t": auc_t,
            "balanced_accuracy_t": balanced_accuracy_t,
            "sensitivity_t": micro_sensitivity_t,
            "specificity_t": micro_specificity_t,
            "score_n": score_n,
            "auc_n": auc_n,
            "balanced_accuracy_n": balanced_accuracy_n,
            "sensitivity_n": micro_sensitivity_n,
            "specificity_n": micro_specificity_n,
            "score_m": score_m,
            "auc_m": auc_m,
            "balanced_accuracy_m": balanced_accuracy_m,
            "sensitivity_m": sensitivity_m,
            "specificity_m": specificity_m,
            "score": score
        }

    write_metrics(metrics=final_metrics)


if __name__ == "__main__":
    main()
