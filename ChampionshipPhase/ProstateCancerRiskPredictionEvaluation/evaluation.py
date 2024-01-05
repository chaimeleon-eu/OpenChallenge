from sklearn import metrics
import math

from evalutils import ClassificationEvaluation
from evalutils.io import CSVLoader


class Prostatecancerriskpredictionevaluation(ClassificationEvaluation):
    def __init__(self):
        super().__init__(
            file_loader=CSVLoader(),
            validators=(),
            join_key="case",
        )

    def score_aggregates(self):

        fpr, tpr, _ = metrics.roc_curve(self._cases["risk_score_ground_truth"], self._cases["risk_score_prob"],
                                        pos_label=1)  # positive class is 1; negative class is 0
        auc = metrics.auc(fpr, tpr)
        if math.isnan(auc):
            auc = 0
        balanced_accuracy = metrics.balanced_accuracy_score(self._cases["risk_score_ground_truth"], self._cases["risk_score_prediction"])
        f1_score = metrics.f1_score(self._cases["risk_score_ground_truth"], self._cases["risk_score_prediction"])
        sensitivity = metrics.recall_score(self._cases["risk_score_ground_truth"], self._cases["risk_score_prediction"])
        tn, fp, fn, tp = metrics.confusion_matrix(self._cases["risk_score_ground_truth"], self._cases["risk_score_prediction"]).ravel()
        specificity = tn / (tn + fp)
        score = 0.4 * auc + 0.2 * sensitivity + 0.2 * specificity + 0.2 * balanced_accuracy

        return {
            "score": score,
            "auc": auc,
            "balanced_accuracy": balanced_accuracy,
            "f1_score": f1_score,
            "sensitivity": sensitivity,
            "specificity": specificity
        }


if __name__ == "__main__":
    Prostatecancerriskpredictionevaluation().evaluate()
