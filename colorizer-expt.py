import requests
import shutil
from pathlib import Path
from secrets import DEEPAI_API_KEY

image_name = "trenchwarfare2-original.jpg"
output_name = image_name.replace("original", "colorized")
original_url = Path(f"images/{image_name}")
output_url = Path(f"images/{output_name}")

r = requests.post(
    "https://api.deepai.org/api/colorizer",
    files={
        'image': open(original_url, 'rb'),
    },
    headers={'api-key': DEEPAI_API_KEY}
)

imageResult = requests.get(r.json()['output_url'], stream=True)
if imageResult.status_code == 200:
    with open(output_url, 'wb') as output_file:
        imageResult.raw.decode_content = True
        shutil.copyfileobj(imageResult.raw, output_file)
else:
    print(f"image result status code: {imageResult.status_code}")
