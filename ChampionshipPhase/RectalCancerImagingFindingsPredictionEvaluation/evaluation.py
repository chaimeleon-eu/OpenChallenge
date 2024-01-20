from pathlib import Path
from pandas import merge, DataFrame
import json
from sklearn import metrics
import math

from evalutils.io import CSVLoader

_VAL_NUMBER_CASES = 34
_TEST_NUMBER_CASES = 66

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

    # Extramural vascular invasion (evi)
    fpr, tpr, _ = metrics.roc_curve(cases["extramural_vascular_invasion_ground_truth"],
                                    cases["extramural_vascular_invasion_prob"],
                                    pos_label=1)  # positive class is 1; negative class is 0
    auc_evi = metrics.auc(fpr, tpr)
    if math.isnan(auc_evi):
        auc_evi = 0
    balanced_accuracy_evi = metrics.balanced_accuracy_score(cases["extramural_vascular_invasion_ground_truth"],
                                                            cases["extramural_vascular_invasion_prediction"])
    f1_score_evi = metrics.f1_score(cases["extramural_vascular_invasion_ground_truth"],
                                    cases["extramural_vascular_invasion_prediction"])
    sensitivity_evi = metrics.recall_score(cases["extramural_vascular_invasion_ground_truth"],
                                           cases["extramural_vascular_invasion_prediction"])
    tn, fp, fn, tp = metrics.confusion_matrix(cases["extramural_vascular_invasion_ground_truth"],
                                              cases["extramural_vascular_invasion_prediction"]).ravel()
    specificity_evi = tn / (tn + fp)
    score_evi = 0.4 * auc_evi + 0.2 * sensitivity_evi + 0.2 * specificity_evi + 0.2 * balanced_accuracy_evi
    print(f'Score EVI: {score_evi}')

    # Mesorectal fascia invasion (mfi)
    fpr, tpr, _ = metrics.roc_curve(cases["mesorectal_fascia_invasion_ground_truth"],
                                    cases["mesorectal_fascia_invasion_prob"],
                                    pos_label=1)  # positive class is 1; negative class is 0
    auc_mfi = metrics.auc(fpr, tpr)
    if math.isnan(auc_mfi):
        auc_mfi = 0
    balanced_accuracy_mfi = metrics.balanced_accuracy_score(
        cases["mesorectal_fascia_invasion_ground_truth"],
        cases["mesorectal_fascia_invasion_prediction"])
    f1_score_mfi = metrics.f1_score(cases["mesorectal_fascia_invasion_ground_truth"],
                                    cases["mesorectal_fascia_invasion_prediction"])
    sensitivity_mfi = metrics.recall_score(cases["mesorectal_fascia_invasion_ground_truth"],
                                           cases["mesorectal_fascia_invasion_prediction"])
    tn, fp, fn, tp = metrics.confusion_matrix(cases["mesorectal_fascia_invasion_ground_truth"],
                                              cases["mesorectal_fascia_invasion_prediction"]).ravel()
    specificity_mfi = tn / (tn + fp)
    score_mfi = 0.4 * auc_mfi + 0.2 * sensitivity_mfi + 0.2 * specificity_mfi + 0.2 * balanced_accuracy_mfi
    print(f'Score MFI: {score_mfi}')

    # Final score
    score = 0.5 * score_evi + 0.5 * score_mfi
    print(f'Final score: {score}')

    final_metrics = dict()
    final_metrics["aggregates"] = {
            "score_evi": score_evi,
            "auc_evi": auc_evi,
            "balanced_accuracy_evi": balanced_accuracy_evi,
            "f1_score_evi": f1_score_evi,
            "sensitivity_evi": sensitivity_evi,
            "specificity_evi": specificity_evi,
            "score_mfi": score_mfi,
            "auc_mfi": auc_mfi,
            "balanced_accuracy_mfi": balanced_accuracy_mfi,
            "f1_score_mfi": f1_score_mfi,
            "sensitivity_mfi": sensitivity_mfi,
            "specificity_mfi": specificity_mfi,
            "score": score
        }

    write_metrics(metrics=final_metrics)


if __name__ == "__main__":
    main()
