# LungCancerOSPrediction Algorithm

The source code for the algorithm container for
LungCancerOSPrediction, generated with
evalutils version 0.4.2
using Python 3.9.

Here you can find an example on how to build your inference code for the
prostate challenge.

The model uses two main inputs:
- Chest CT (*chest-ct*), corresponding to the image in mha format.
  - Clinical data (*clinical-information-lung-ct*), which includes the patient age, gender, smoking status, clinical category, regional nodes category and metastasis category (TNM).

Then, after overall survival prediction, the model has to provide one main output:
- Predicted survival time in months (*overall-survival-months.json*).

In the [main](process.py) file you will find an example on how to read the input data and how to generate the output file. 
Outputs are generated **randomly** as an example.

## Build the Docker image
To build the docker image open a terminal and change your directory to the *LungCancerOSPrediction* folder.
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
This is the file you have to upload to grand challenge when submitting a new algorithm.
