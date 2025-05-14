import os,requests,json
from PIL import Image
from io import BytesIO
import pillow_avif


with open("./items.json", "r", encoding="utf-8") as fp:
    items = json.load(fp)

def download_images(items):
    for item in items:
        name = item['name']
        url = item['image']
        size = item['size'] #Split Small Medium and Large Items into different folders

        safe_name = "".join([c if c.isalnum() else '_' for c in name]).strip('_')
        folder = f"item_images/{size}"
        filename = f"item_images/{size}/{safe_name}.png"

        os.makedirs(folder, exist_ok=True)
        
        if not os.path.exists(filename):
            try:
                response = requests.get(url)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                img.save(filename, format="PNG")
                print(f"Saved: {filename}")
            except Exception as e:
                print(f"Failed to save {name}: {e}")

if __name__ == "__main__":
    print("downloading images")
    download_images(items)