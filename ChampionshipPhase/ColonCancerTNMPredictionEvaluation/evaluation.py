from sklearn import metrics
import math
import numpy as np

from evalutils import ClassificationEvaluation
from evalutils.io import CSVLoader


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


class Coloncancertnmpredictionevaluation(ClassificationEvaluation):
    def __init__(self):
        super().__init__(
            file_loader=CSVLoader(),
            validators=(),
            join_key="case",
        )

    def score_aggregates(self):

        # Tumor pathological category (T)
        y_test = self._cases["t_ground_truth"]
        y_pred_prob_t1 = self._cases["t1_prob"]
        y_pred_prob_t2 = self._cases["t2_prob"]
        y_pred_prob_t3 = self._cases["t3_prob"]
        y_pred_prob_t4a = self._cases["t4a_prob"]
        y_pred_prob_t4b = self._cases["t4b_prob"]

        y_pred_prob = np.column_stack((y_pred_prob_t1, y_pred_prob_t2, y_pred_prob_t3, y_pred_prob_t4a, y_pred_prob_t4b))

        auc_t = metrics.roc_auc_score(y_test, y_pred_prob, multi_class='ovr')

        micro_sensitivity_t = metrics.recall_score(self._cases["t_ground_truth"],
                                                   self._cases["t_prediction"],
                                                   average='micro')

        micro_specificity_t = micro_specificity_calculation(self._cases["t_ground_truth"],
                                                   self._cases["t_prediction"],
                                                   classes = [0, 1, 2, 3, 4])

        balanced_accuracy_t = metrics.balanced_accuracy_score(self._cases["t_ground_truth"],
                                                              self._cases["t_prediction"])

        score_t = 0.4 * auc_t + 0.2 * micro_sensitivity_t + 0.2 * micro_specificity_t + 0.2 * balanced_accuracy_t

        # Regional nodes pathological category (N)
        y_test = self._cases["n_ground_truth"]
        y_pred_prob_n0 = self._cases["n0_prob"]
        y_pred_prob_n1 = self._cases["n1_prob"]
        y_pred_prob_n2 = self._cases["n2_prob"]

        y_pred_prob = np.column_stack(
            (y_pred_prob_n0, y_pred_prob_n1, y_pred_prob_n2))

        auc_n = metrics.roc_auc_score(y_test, y_pred_prob, multi_class='ovr')

        micro_sensitivity_n = metrics.recall_score(self._cases["n_ground_truth"],
                                                   self._cases["n_prediction"],
                                                   average='micro')

        micro_specificity_n = micro_specificity_calculation(self._cases["n_ground_truth"],
                                                            self._cases["n_prediction"],
                                                            classes=[0, 1, 2])

        balanced_accuracy_n = metrics.balanced_accuracy_score(self._cases["n_ground_truth"],
                                                              self._cases["n_prediction"])

        score_n = 0.4 * auc_n + 0.2 * micro_sensitivity_n + 0.2 * micro_specificity_n + 0.2 * balanced_accuracy_n

        # Metastasis pathological category (M)

        fpr, tpr, _ = metrics.roc_curve(self._cases["m_ground_truth"], self._cases["m_prob"],
                                        pos_label=1)  # positive class is 1; negative class is 0
        auc_m = metrics.auc(fpr, tpr)
        if math.isnan(auc_m):
            auc_m = 0
        balanced_accuracy_m = metrics.balanced_accuracy_score(self._cases["m_ground_truth"],
                                                              self._cases["m_prediction"])
        f1_score_m = metrics.f1_score(self._cases["m_ground_truth"], self._cases["m_prediction"])
        sensitivity_m = metrics.recall_score(self._cases["m_ground_truth"], self._cases["m_prediction"])
        tn, fp, fn, tp = metrics.confusion_matrix(self._cases["m_ground_truth"],
                                                  self._cases["m_prediction"]).ravel()
        specificity_m = tn / (tn + fp)
        score_m = 0.4 * auc_m + 0.2 * sensitivity_m + 0.2 * specificity_m + 0.2 * balanced_accuracy_m

        # Final score
        score = 0.4 * score_t + 0.3 * score_n + 0.3 * score_m

        return {
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


if __name__ == "__main__":
    Coloncancertnmpredictionevaluation().evaluate()
