import SimpleITK as sitk
from pathlib import Path
import json
import random

from evalutils import ClassificationAlgorithm
from evalutils.validators import (
    UniquePathIndicesValidator,
    UniqueImagesValidator,
)


class Prostatecancerriskprediction(ClassificationAlgorithm):
    def __init__(self):
        super().__init__(
            validators=dict(
                input_image=(
                    UniqueImagesValidator(),
                    UniquePathIndicesValidator(),
                )
            ),
        )

        # path to image file
        self.image_input_dir = "/input/images/axial-t2-prostate-mri/"
        self.image_input_path = list(Path(self.image_input_dir).glob("*.mha"))[0]

        # load clinical information
        with open("/input/clinical-information-prostate-mri.json") as fp:
            self.clinical_info = json.load(fp)

        # path to output files
        self.risk_score_output_file = Path("/output/prostate-cancer-risk-score.json")
        self.risk_score_likelihood_output_file = Path("/output/prostate-cancer-risk-score-likelihood.json")
    
    def predict(self):
        """
        Your algorithm goes here
        """        
        
        # read image
        image = sitk.ReadImage(str(self.image_input_path))
        clinical_info = self.clinical_info
        print('Clinical info: ')
        print(clinical_info)

        # TODO: Add your inference code here

        # our code generates a random probability
        risk_score_likelihood = random.random()
        if risk_score_likelihood > 0.5:
            risk_score = 'High'
        else:
            risk_score = 'Low'
        print('Risk score: ', risk_score)
        print('Risk score likelihood: ', risk_score_likelihood)

        # save case-level class
        with open(str(self.risk_score_output_file), 'w') as f:
            json.dump(risk_score, f)

        # save case-level likelihood
        with open(str(self.risk_score_likelihood_output_file), 'w') as f:
            json.dump(float(risk_score_likelihood), f)


if __name__ == "__main__":
    Prostatecancerriskprediction().predict()
