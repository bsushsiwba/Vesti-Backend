from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from PIL import Image
import io
import os
import time
from enum import Enum
import shutil


class ClothingType(str, Enum):
    upper_body = "upper_body"
    lower_body = "lower_body"
    dresses = "dresses"


app = FastAPI()


@app.post("/tryon/")
async def create_tryon(
    human: UploadFile = File(...),
    garment: UploadFile = File(...),
    clothing_type: ClothingType = ClothingType.upper_body,
):
    try:
        # Save human image
        with open("human.png", "wb") as f:
            shutil.copyfileobj(human.file, f)

        # Save garment image
        with open("garment.png", "wb") as f:
            shutil.copyfileobj(garment.file, f)

        # Write process.txt with clothing type
        with open("process.txt", "w") as f:
            f.write(clothing_type)

        # Wait for result (timeout after 30 seconds)
        timeout = 30
        start_time = time.time()
        while not os.path.exists("result.png"):
            if time.time() - start_time > timeout:
                raise HTTPException(status_code=408, detail="Processing timeout")
            time.sleep(0.1)

        # Check if there was an error
        if os.path.exists("complete.txt"):
            with open("complete.txt", "r") as f:
                status = f.read().strip()
                if status.startswith("error"):
                    raise HTTPException(status_code=500, detail=status)

        # Read and return result image
        img = Image.open("result.png")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        # Cleanup
        if os.path.exists("result.png"):
            os.remove("result.png")
        if os.path.exists("complete.txt"):
            os.remove("complete.txt")

        return Response(content=img_byte_arr, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
