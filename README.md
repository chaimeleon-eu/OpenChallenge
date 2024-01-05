# ChAImeleon Open Challenges

The ChAImeleon Open Challenges is a competition designed to train 
and refine AI models to answer clinical questions about five types 
of cancer: prostate, lung, breast, colon, and rectal. 
Participants are challenged to collaborate and develop innovative
AI-powered solutions that can significantly impact cancer diagnosis, 
management, and treatment. 

You can find more information in the following link: https://chaimeleon.grand-challenge.org/overview/

This repository includes some example scripts to build the inference code for
the evaluation of your models in both the Validation and Test phases of the 
Classification phase using grand-challenge platform.
- Inference:
  - [Prostate Challenge](ClassificationPhase/ProstateCancerRiskPrediction/README.md)
  - [Lung Challenge](ClassificationPhase/LungCancerOSPrediction/README.md)
- Evaluation:
  - [Prostate Challenge](ClassificationPhase/ProstateCancerRiskPredictionEvaluation/README.md)
  - [Lung Challenge](ClassificationPhase/LungCancerOSPredictionEvaluation/README.md)

You can also find the evaluation scripts for the Championship phase:
- [Prostate Challenge](ChampionshipPhase/ProstateCancerRiskPredictionEvaluation/README.md)
- [Lung Challenge](ChampionshipPhase/LungCancerOSPredictionEvaluation/README.md)
- [Rectum Challenge](ChampionshipPhase/RectalCancerImagingFindingsPredictionEvaluation/README.md)
- [Colon Challenge](ChampionshipPhase/ColonCancerTNMPredictionEvaluation/README.md)
- [Breast Challenge](ChampionshipPhase/BreastCancerHistologySubtypePredictionEvaluation/README.md)

Finally, it includes an example per cancer type of the CSV file to submit during the Championship phase
to GrandChallenge for your models' evaluation. You can find them in the following [folder](ChampionshipPhase/submission_csv_examples).


