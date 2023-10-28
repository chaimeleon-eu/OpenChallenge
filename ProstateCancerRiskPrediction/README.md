# ProstateCancerRiskPrediction Algorithm

The source code for the algorithm container for
ProstateCancerRiskPrediction, generated with
evalutils version 0.4.2
using Python 3.9.

Here you can find an example on how to build your inference code for the
prostate challenge.

The model uses two main inputs:
- Prostate T2w MRI (*axial-t2-prostate-mri*), corresponding to the image in mha format.
- Clinical data (*clinical-information-prostate-mri.json*), which includes the patient age and PSA.

Then, after risk prediction, the model has to provide two main output:
- The risk score (*prostate-cancer-risk-score.json*) which can have the values "Low" or "High".
- The risk score likelihood (*prostate-cancer-risk-score-likelihood.json*) which represents the probability given by the model.

In the [main](process.py) file you will find an example on how to read the input data and how to generate the output files. 
Outputs are generated **randomly** as an example.

## Build the Docker image
To build the docker image open a terminal and change your directory to the *ProstateCancerRiskPrediction* folder.
Then run the following command:
```
docker build -f Dockerfile -t <your_docker_image_name> .
```
Change ```<your_docker_image_name>``` by the name you want the Docker image to have.

Finally, to submit your Docker image to grand-challenge you need to encapsulate it in a file.
The generate the file to upload, run the following command:
```
docker save -o <output_file_name>.tar.gz <your_docker_image_name>
```
With this command, a file named <output_file_name>.tar.gz will be generated. 
This is the file you have to upload to grand challenge when submitting a new algorithm
