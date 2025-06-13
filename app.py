from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from PIL import Image
import io
import os
import time
from enum import Enum
import shutil
import requests


class ClothingType(str, Enum):
    upper_body = "upper_body"
    lower_body = "lower_body"
    dresses = "dresses"


def download_image(url: str) -> Image.Image:
    """Download image from URL, downsample if needed, and return as a PIL Image."""
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=400, detail=f"Failed to download image from {url}"
        )

    print("Image downloaded")
    img = Image.open(io.BytesIO(response.content))

    # Check dimensions and downsample if necessary
    max_dimension = max(img.size)
    if max_dimension > 600:
        scale_factor = 600 / max_dimension
        new_width = int(img.size[0] * scale_factor)
        new_height = int(img.size[1] * scale_factor)
        img = img.resize(
            (new_width, new_height), Image.Resampling.LANCZOS
        )  # Use LANCZOS for high-quality downsampling
        print(f"Image downsampled to: {new_width}x{new_height}")
    else:
        print("Image dimensions within limit, no downsampling required")

    return img


app = FastAPI()


@app.post("/tryon-dev/")
async def create_tryon_dev(
    human: UploadFile = File(...),
    garment: UploadFile = File(...),
    clothing_type: ClothingType = ClothingType.upper_body,
):
    try:
        if os.path.exists("complete.txt"):
            os.remove("complete.txt")

        # Save human image
        with open("human.png", "wb") as f:
            shutil.copyfileobj(human.file, f)

        # Save garment image
        with open("garment.png", "wb") as f:
            shutil.copyfileobj(garment.file, f)

        # Write process.txt with clothing type
        with open("process.txt", "w") as f:
            f.write(clothing_type)

        while not os.path.exists("complete.txt"):
            time.sleep(0.1)

        # Read and return result image
        img = Image.open("result.png")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        # Cleanup
        if os.path.exists("result.png"):
            os.remove("result.png")

        return Response(content=img_byte_arr, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tryon/")
async def create_tryon(
    garment: str,
    human: UploadFile = File(...),
    clothing_type: ClothingType = ClothingType.upper_body,
):
    try:
        if os.path.exists("complete.txt"):
            os.remove("complete.txt")

        # Download and save human image
        with open("human.png", "wb") as f:
            shutil.copyfileobj(human.file, f)

        # Download garment image from URL
        img = download_image(garment)
        img.save("garment.png")

        # Write process.txt with clothing type
        with open("process.txt", "w") as f:
            f.write(clothing_type)

        while not os.path.exists("complete.txt"):
            time.sleep(0.1)

        # Read and return result image
        img = Image.open("result.png")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        # Cleanup
        if os.path.exists("result.png"):
            os.remove("result.png")

        return Response(content=img_byte_arr, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
