import requests
import shutil
from pathlib import Path
from secrets import DEEPAI_API_KEY
from os.path import basename, splitext


def colorize(image_path, save_path, API_KEY):
    deepai_res = requests.post(
        "https://api.deepai.org/api/colorizer",
        files={"image": open(image_path, "rb")},
        headers={"api-key": API_KEY},
    )

    colorized_image_url = requests.get(deepai_res.json()["output_url"], stream=True)
    if colorized_image_url.status_code == 200:
        with open(save_path, "wb") as save_file:
            colorized_image_url.raw.decode_content = True
            shutil.copyfileobj(colorized_image_url.raw, save_file)
    else:
        print(f"image result status code: {colorized_image_url.status_code}")


images_dir = Path("images")
original_dir = images_dir / "original-images"
output_dir = images_dir / "colorized-images"

all_input_images = original_dir.glob("*jpg")
for input_image in all_input_images:
    output_name = splitext(basename(input_image))[0] + "_color.jpg"
    output_path = output_dir / output_name
    if not output_path.exists():
        print(f"Colorizing '{basename(input_image)}'...")
        colorize(input_image, output_path, DEEPAI_API_KEY)
