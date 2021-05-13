from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import shutil
from typing import List
import os

app = FastAPI()


@app.post("/files")
async def create_file(file: bytes = File(...)):
    return {
        "file_size": len(file)
    }


@app.post("/singlefile")
async def upload_file(files: UploadFile = File(...)):
    fileUpload = f'./upload/{files.filename}'
    with open(fileUpload, "wb") as buffer:
        shutil.copyfileobj(files.file, buffer)

    f = open(fileUpload)
    f.seek(0, os.SEEK_END)

    return {
        "filename": files.filename,
        "sizeInMegaBytes": (os.stat(fileUpload).st_size / (1024 * 1024)),
        "sizeInBytes": f.tell()
    }


@app.post("/multiplefile")
async def upload_img_file(files: List[UploadFile] = File(...)):
    for file in files:
        with open(f'./upload/{file.filename}', "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {
        "uploadfile": [[f.filename, f] for f in files]
    }


@app.get("/")
async def main():
    content = """
    <body>
    <H1>Single File</H1>
    <form action="/singlefile/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <H1>Multiple Files</H1>
    <form action="/multiplefile/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)
