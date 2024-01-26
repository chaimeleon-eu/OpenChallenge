# CSV files for Championship phase evaluation

Here you can find an example per cancer type of the CSV file to submit to GrandChallenge for the evaluation
(both validation and test phases) of your algorithms.
Each file include de column `case` where you have to specify the ChAImeleon patient ID. You will find this ID
in the `eforms.json` file which also corresponds to the patient folder name.

Then, for each cancer type, you will find the following columns:
* Prostate cancer
  * *risk_score*: Patient risk score where **0** represents a **Low risk** score while **1** refers to a **High risk** score.
  * *risk_score_prob*: Probability of being a **High risk** patient (positive class) in a range between 0 and 1.
* Lung cancer
  * *survival_time_months*: Patient overall survival time in months
* Rectal cancer:
  * *extramural_vascular_invasion*: Presence of extramural vascular invasion, where **0** refers to **no invasion**, whole **1** refers to **invasion**.
  * *extramural_vascular_invasion_prob*: Probability of extramural vascular invasion.
  * *mesorectal_fascia_invasion*: Presence of mesorectal fascia invasion, where **0** refers to **no invasion**, whole **1** refers to **invasion**.
  * *mesorectal_fascia_invasion_prob*: Probability of mesorectal fascia invasion.
* Colon cancer:
  * *t*: Tumor pathological category (T), whose options with their respective codification are **T1/T2 (0), T3 (1), T4a (2), T4b (3)**.
  * *t1_t2_prob*: Probability associated to the **T1/T2** class in the prediction of tumor pathological category.
  * *t3_prob*: Probability associated to the **T3** class in the prediction of tumor pathological category.
  * *t4a_prob*: Probability associated to the **T4a** class in the prediction of tumor pathological category.
  * *t4b_prob*: Probability associated to the **T4b** class in the prediction of tumor pathological category.
  * *n*: Regional nodes pathological category (N), whose options and their respective codifications are **N0 (0), N1 (1), N2 (2)**.
  * *n0_prob*: Probability associated to the **N0** class in the prediction of regional nodes pathological category.
  * *n1_prob*: Probability associated to the **N1** class in the prediction of regional nodes pathological category.
  * *n2_prob*: Probability associated to the **N2** class in the prediction of regional nodes pathological category.
  * *m*: Metastasis pathological category (M), whose options and their respective codifications are **M0 (0), M1 (1)**
  * *m_prob*: Probability of positive metastasis pathological category (M1).
* Breast cancer:
  * *histology_subtype*: Tumor histology subtype where **1** refers to **Ductal carcinoma in situ (DCIS)**, **2** refers to **Invasive duct carcinoma (IDC)**, **3** refers to **Invasive lobular carcinoma (ILC)**,  and **0** refers to **Other**.
  * *other_prob*: Probability associated to the **Other** class.
  * *dcis_prob*: Probability associated to the **Ductal carcinoma in situ (DCIS)** class.
  * *idc_prob*: Probability associated to the **Invasive duct carcinoma (IDC)** class.
  * *ilc_prob*: Probability associated to the **Invasive lobular carcinoma (ILC)** class.

NOTE: All the probabilities are in a range between 0 and 1.


