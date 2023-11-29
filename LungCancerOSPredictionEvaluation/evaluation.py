import json
from pathlib import Path
from pprint import pprint
from lifelines.utils import concordance_index

import SimpleITK

INPUT_DIRECTORY="/input"  # You can change this to "test_submission" to run outside Docker, but remember to change it back before building your container
OUTPUT_DIRECTORY="/output"  # You can also change this to a local directory to run outside Docker, but remember to change it back

def main():
    print_inputs()

    final_metrics = {"case": {}}
    predictions = read_predictions()
    predictions_os = []
    ground_truth_os = []
    ground_truth_event = []

    for job in predictions:
        # We now iterate over each algorithm job for this submission
        # Note that the jobs are not in any order! We work that out from predictions.json
        # This corresponds to one archive item in the archive
        ct = get_image_name(values=job["inputs"], slug="chest-ct")
        # info = get_image_name(values=job["inputs"], slug="clinical-information-lung-ct")
        
        # Parse one of the filenames to get the batch ID, you could cross-check with the others
        batch_id = ct.split('.')[0]
        print(f"Processing batch {batch_id}")
        print((ct))

        os_months = get_value_from_outputs(outputs=job["outputs"], slug="overall-survival-months")

        # Now you would need to load your ground truth, include it in the evaluation container
        path_ground_truth = Path(__file__).parent / 'ground_truth' / batch_id / f'{batch_id}_ground_truth.json'
        ground_truth = load_json_file(location=str(path_ground_truth))
        print(ground_truth)

        print(f"Predicted OS (months): {os_months}")
        print(f"Ground truth time (months): {ground_truth['survival_time_months']}")
        print(f"Ground truth event: {ground_truth['event']}")

        predictions_os.append(float(os_months))
        ground_truth_os.append(float(ground_truth['survival_time_months']))
        ground_truth_event.append(int(ground_truth['event']))

        print("")

    # Build metrics

    # Calculate the concordance index
    c_index = concordance_index(ground_truth_os, predictions_os, ground_truth_event)

    final_metrics["aggregates"] = {"c_index": c_index}

    pprint(final_metrics)

    write_metrics(metrics=final_metrics)

    return 0


def print_inputs():
    # Just for convenience, in the logs you can then see what files you have to work with
    input_files = [str(x) for x in Path(INPUT_DIRECTORY).rglob("*") if x.is_file()]

    print("Input Files:")
    pprint(input_files)
    print("")


def read_predictions():
    # The predictions file tells us the location of the users predictions
    with open(f"{INPUT_DIRECTORY}/predictions.json") as f:
        return json.loads(f.read())


def get_image_name(*, values, slug):
    # This tells us the user-provided name of the input or output image
    for value in values:
        if value["interface"]["slug"] == slug:
            return value["image"]["name"]
    
    raise RuntimeError(f"Image with interface {slug} not found!")


def get_interface_relative_path(*, values, slug):
    # Gets the location of the interface relative to the input or output
    for value in values:
        if value["interface"]["slug"] == slug:
            return value["interface"]["relative_path"]
    
    raise RuntimeError(f"Value with interface {slug} not found!")


def get_file_location(*, job_pk, values, slug):
    # Where a job's output file will be located in the evaluation container
    relative_path = get_interface_relative_path(values=values, slug=slug)
    return f"{INPUT_DIRECTORY}/{job_pk}/output/{relative_path}"


def get_value_from_outputs(outputs, slug):
    for output in outputs:
        if output['interface']['slug'] == slug:
            return output['value']


def load_json_file(*, location):
    # Reads a json file
    with open(location) as f:
        return json.loads(f.read())


def load_image(*, location):
    mha_files = {f for f in Path(location).glob("*.mha") if f.is_file()}

    if len(mha_files) == 1:
        mha_file = mha_files.pop()
        return SimpleITK.ReadImage(mha_file)
    elif len(mha_files) > 1:
        raise RuntimeError(
            f"More than one mha file was found in {location!r}"
        )
    else:
        raise NotImplementedError


def write_metrics(*, metrics):
    # Write a json document that is used for ranking results on the leaderboard
    with open("/output/metrics.json", "w") as f:
        f.write(json.dumps(metrics))


if __name__ == "__main__":
    raise SystemExit(main())
