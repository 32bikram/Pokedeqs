from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, status

router = APIRouter(
    tags = ['Uploading'],
    prefix = "/upload"
)

allowed_extension = {"image/png", "image/jpg", "image/jpeg"}

@router.post("/")
async def upload_file(file : UploadFile = File(...)):
    if(file == None):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No file uploaded"
        )

    if file.content_type not in allowed_extension:
        raise HTTPException(
            status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail = "File isnt an image" 
        )
    
    image_bytes = await file.read()
    if(len(image_bytes) == 0):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No file uploaded"
        )
    
    return {
        "filename" : file.filename,
        "content_type" : file.content_type,
        "file_size" : len(image_bytes)
    }