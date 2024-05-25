from utils import build_flashcards
from argparse import ArgumentParser
import shutil
from pathlib import Path

CAR_DICT = {
    "Alertness": "https://api.theorypass.co.uk/theory/quizzes/car/get/alertness",
    "Attitude": "https://api.theorypass.co.uk/theory/quizzes/car/get/attitude",
    "Safety and Your Vehicle": "https://api.theorypass.co.uk/theory/quizzes/car/get/safety-and-your-vehicle",
    "Safety Margins": "https://api.theorypass.co.uk/theory/quizzes/car/get/safety-margins",
    "Hazard Awareness": "https://api.theorypass.co.uk/theory/quizzes/car/get/essential-documents",
    "Vulnerable Road Users": "https://api.theorypass.co.uk/theory/quizzes/car/get/vehicle-loading",
    "Other Types of Vehicle": "https://api.theorypass.co.uk/theory/quizzes/car/get/other-types-of-vehicle",
    "Vehicle Handling": "https://api.theorypass.co.uk/theory/quizzes/car/get/vehicle-handling",
    "Motorway Rules": "https://api.theorypass.co.uk/theory/quizzes/car/get/motorway-rules",
    "Rules of the Road": "https://api.theorypass.co.uk/theory/quizzes/car/get/rules-of-the-road",
    "Road and Traffic Signs": "https://api.theorypass.co.uk/theory/quizzes/car/get/road-and-traffic-signs",
    "Essential Documents": "https://api.theorypass.co.uk/theory/quizzes/car/get/essential-documents",
    "Incidents, Accidents, and Emergencies": "https://api.theorypass.co.uk/theory/quizzes/car/get/incidents-accidents-and-emergencies",
    "Vehicle Loading": "https://api.theorypass.co.uk/theory/quizzes/car/get/vehicle-loading",
}

MOTORBIKE_DICT = {
    "Alertness": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/alertness",
    "Attitude": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/attitude",
    "Safety and Your Vehicle": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/safety-and-your-vehicle",
    "Safety Margins": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/safety-margins",
    "Hazard Awareness": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/essential-documents",
    "Vulnerable Road Users": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/vehicle-loading",
    "Other Types of Vehicle": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/other-types-of-vehicle",
    "Vehicle Handling": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/vehicle-handling",
    "Motorway Rules": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/motorway-rules",
    "Rules of the Road": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/rules-of-the-road",
    "Road and Traffic Signs": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/road-and-traffic-signs",
    "Essential Documents": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/essential-documents",
    "Incidents, Accidents, and Emergencies": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/incidents-accidents-and-emergencies",
    "Vehicle Loading": "https://api.theorypass.co.uk/theory/quizzes/motorcycle/get/vehicle-loading",
}

LORRY_DICT = {
    "Braking Systems": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/braking-systems",
    "Drivers' Hours and Rest Periods": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/drivers-hours-and-rest-periods",
    "Environmental Issues": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/environmental-issues",
    "Essential Documents": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/essential-documents",
    "Incidents, Accidents, and Emergencies" : "https://api.theorypass.co.uk/theory/quizzes/hgv/get/incidents-accidents-and-emergencies",
    "Leaving the Vehicle": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/leaving-the-vehicle",
    "Other Road Users": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/other-road-users",
    "Restricted View": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/restricted-view",
    "Road and Traffic Signs": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/road-and-traffic-signs",
    "The Driver": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/the-driver",
    "The Road": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/the-road",
    "Vehicle Condition": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/vehicle-condition",
    "Vehicle Loading": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/vehicle-loading",
    "Vehicle Weights and Dimensions": "https://api.theorypass.co.uk/theory/quizzes/hgv/get/vehicle-weights-and-dimensions"
}

BUS_DICT = {
    "Braking Systems": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/braking-systems",
    "Carrying Passengers": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/carrying-passengers",
    "Drivers' Hours and Rest Periods": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/drivers-hours-and-rest-periods",
    "Environmental Issues": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/environmental-issues",
    "Essential Documents": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/essential-documents",
    "Incidents, Accidents, and Emergencies" : "https://api.theorypass.co.uk/theory/quizzes/pcv/get/incidents-accidents-and-emergencies",
    "Leaving the Vehicle": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/leaving-the-vehicle",
    "Other Road Users": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/other-road-users",
    "Restricted View": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/restricted-view",
    "Road and Traffic Signs": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/road-and-traffic-signs",
    "The Driver": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/the-driver",
    "The Road": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/the-road",
    "Vehicle Condition": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/vehicle-condition",
    "Vehicle Weights and Dimensions": "https://api.theorypass.co.uk/theory/quizzes/pcv/get/vehicle-weights-and-dimensions"
}

ADI_DICT = {
    "Driving Test, Disabilities, Law": "https://api.theorypass.co.uk/theory/quizzes/adi/get/driving-test-disabilities-law",
    "Signs, Signals, and Control": "https://api.theorypass.co.uk/theory/quizzes/adi/get/traffic-signs-and-signals-car-control-pedestrians-mechanical-knowledge",
    "Publications, Instructionals Techniques": "https://api.theorypass.co.uk/theory/quizzes/adi/get/publications-instructional-techniques",
    "Road Procedure": "https://api.theorypass.co.uk/theory/quizzes/adi/get/road-procedure",
}

MAIN_DICT = {
    "car": CAR_DICT,
    "motorbike": MOTORBIKE_DICT,
    "lorry": LORRY_DICT,
    "bus": BUS_DICT,
    "adi": ADI_DICT
}

parser = ArgumentParser()
parser.add_argument("--clean", action="store_true",
                    help="cleans up /temp/. Must be run in ./src/. Will not build flashcards if this option is provided.")
parser.add_argument("vehicles", nargs="*",
                    help="List of test types to construct flashcards for.\nOptions are car, motorbike, lorry, bus, adi. If none provided, all will be constructed.")

args = parser.parse_args()

if args.clean:
    dirpath = Path('./temp')
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    print("Cleaned up temp")
    exit(0)


if args.vehicles == []:
    for test, urldict in MAIN_DICT.items():
        build_flashcards(urldict, test)

elif len(args.vehicles) > 5:
    raise ValueError("Too many arguments provided")

else:
    for arg in args.vehicles:
        if arg in ["car", "motorbike", "lorry", "bus", "adi"]:
            build_flashcards(MAIN_DICT[arg], arg)
        else:
            raise ValueError(f"""Invalid argument provided: {arg}.
                             Valid options are: car, lorry, bus, adi, motorbike""")
