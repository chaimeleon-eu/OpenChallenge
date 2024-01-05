from sklearn import metrics
import math

from evalutils import ClassificationEvaluation
from evalutils.io import CSVLoader


class Rectalcancerimagingfindingspredictionevaluation(ClassificationEvaluation):
    def __init__(self):
        super().__init__(
            file_loader=CSVLoader(),
            validators=(),
            join_key="case",
        )

    def score_aggregates(self):

        # Extramural vascular invasion (evi)
        fpr, tpr, _ = metrics.roc_curve(self._cases["extramural_vascular_invasion_ground_truth"],
                                        self._cases["extramural_vascular_invasion_prob"],
                                        pos_label=1)  # positive class is 1; negative class is 0
        auc_evi = metrics.auc(fpr, tpr)
        if math.isnan(auc_evi):
            auc_evi = 0
        balanced_accuracy_evi = metrics.balanced_accuracy_score(self._cases["extramural_vascular_invasion_ground_truth"],
                                                                self._cases["extramural_vascular_invasion_prediction"])
        f1_score_evi = metrics.f1_score(self._cases["extramural_vascular_invasion_ground_truth"],
                                        self._cases["extramural_vascular_invasion_prediction"])
        sensitivity_evi = metrics.recall_score(self._cases["extramural_vascular_invasion_ground_truth"],
                                               self._cases["extramural_vascular_invasion_prediction"])
        tn, fp, fn, tp = metrics.confusion_matrix(self._cases["extramural_vascular_invasion_ground_truth"],
                                                  self._cases["extramural_vascular_invasion_prediction"]).ravel()
        specificity_evi = tn / (tn + fp)
        score_evi = 0.4 * auc_evi + 0.2 * sensitivity_evi + 0.2 * specificity_evi + 0.2 * balanced_accuracy_evi

        # Mesorectal fascia invasion (mfi)
        fpr, tpr, _ = metrics.roc_curve(self._cases["mesorectal_fascia_invasion_ground_truth"],
                                        self._cases["mesorectal_fascia_invasion_prob"],
                                        pos_label=1)  # positive class is 1; negative class is 0
        auc_mfi = metrics.auc(fpr, tpr)
        if math.isnan(auc_mfi):
            auc_mfi = 0
        balanced_accuracy_mfi = metrics.balanced_accuracy_score(
            self._cases["mesorectal_fascia_invasion_ground_truth"],
            self._cases["mesorectal_fascia_invasion_prediction"])
        f1_score_mfi = metrics.f1_score(self._cases["mesorectal_fascia_invasion_ground_truth"],
                                        self._cases["mesorectal_fascia_invasion_prediction"])
        sensitivity_mfi = metrics.recall_score(self._cases["mesorectal_fascia_invasion_ground_truth"],
                                               self._cases["mesorectal_fascia_invasion_prediction"])
        tn, fp, fn, tp = metrics.confusion_matrix(self._cases["mesorectal_fascia_invasion_ground_truth"],
                                                  self._cases["mesorectal_fascia_invasion_prediction"]).ravel()
        specificity_mfi = tn / (tn + fp)
        score_mfi = 0.4 * auc_mfi + 0.2 * sensitivity_mfi + 0.2 * specificity_mfi + 0.2 * balanced_accuracy_mfi

        # Final score
        score = 0.5 * score_evi + 0.5 * score_mfi

        return {
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


if __name__ == "__main__":
    Rectalcancerimagingfindingspredictionevaluation().evaluate()
