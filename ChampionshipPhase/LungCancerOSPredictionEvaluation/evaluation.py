from lifelines.utils import concordance_index

from evalutils import ClassificationEvaluation
from evalutils.io import CSVLoader


class Lungcancerospredictionevaluation(ClassificationEvaluation):
    def __init__(self):
        super().__init__(
            file_loader=CSVLoader(),
            validators=(),
            join_key="case",
        )

    def score_aggregates(self):
        c_index = concordance_index(self._cases["overall_survival_months_ground_truth"],
                                    self._cases["overall_survival_months_prediction"],
                                    self._cases["event"])
        return {
            "c-index": c_index,
        }


if __name__ == "__main__":
    Lungcancerospredictionevaluation().evaluate()
