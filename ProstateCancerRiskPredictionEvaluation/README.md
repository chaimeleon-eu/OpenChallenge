# ProstateCancerRiskPredictionEvaluation

The source code for the evaluation container for
ProstateCancerRiskPrediction, generated with
evalutils version 0.4.2
using Python 3.9.

This section includes the code used to evaluate the submissions of the prostate task.
The code includes the whole container to have a general overview on the execution of the evaluation process.
At the end, you can find the specific metrics extracted. These include:

- Area Under the ROC Curve (AUC)
- Sensitivity
- Specificity
- Balanced Accuracy

Finally, the leaderboard is updated according to a generic score calculated from the previous metrics as:

Sore = 0.4 * AUC + 0.2 * Sensitivity + 0.2 * Specificity + 0.2 * Balanced Accuracy
