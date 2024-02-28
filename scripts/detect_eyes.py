import cv2
import dlib
import os
import json
from collections import defaultdict
import pprint


folder_path = "/home/joao/StreamHelperAssets/games/tekken8/vs_renders"

game_config = json.load(
    open(f"{folder_path}/../base_files/config.json"))
asset_config = json.load(
    open(f"{folder_path}/config.json"))


def get_eye_positions(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale for Haar Cascade
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained facial landmarks predictor from dlib
    # You need to download this file
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)

    # Detect faces in the image
    faces = dlib.get_frontal_face_detector()(gray_image)

    eyes = []

    # Iterate over detected faces and print eye positions
    for face in faces:
        landmarks = predictor(gray_image, face)

        # Extract eye landmarks
        left_eye = (landmarks.part(36).x, landmarks.part(36).y)
        right_eye = (landmarks.part(45).x, landmarks.part(45).y)

        eyes.append(left_eye)
        eyes.append(right_eye)

    return eyes


prefix = asset_config.get("prefix")
postfix = asset_config.get("postfix")

images = os.listdir(folder_path)

# character -> skin -> x/y -> pos
output = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

for character in game_config["character_to_codename"].values():
    codename = character.get("codename")

    char_images = [i for i in images if i.startswith(
        f"{prefix}{codename}{postfix}")]

    for char_img in char_images:
        filename = char_img.split(".")[0]
        second_part = filename.split(f"{prefix}{codename}{postfix}")[1]

        is_flipped = False

        if "_FLIPPED" in second_part:
            is_flipped = True
            second_part = second_part.replace("_FLIPPED", "")

        skin = 0

        try:
            skin = int(second_part)
        except:
            pass

        print(codename, skin, is_flipped)

        eyes = get_eye_positions(f"{folder_path}/{char_img}")

        xx = []
        yy = []

        if len(eyes) > 0:
            for (x, y) in eyes:
                xx.append(x)
                yy.append(y)

            output[codename][str(skin) +
                             "_FLIPPED" if is_flipped else skin]["x"] = int(sum(xx)/len(xx))
            output[codename][str(skin) +
                             "_FLIPPED" if is_flipped else skin]["y"] = int(sum(yy)/len(yy))

pprint.pprint(json.loads(json.dumps(output)))

exit()
