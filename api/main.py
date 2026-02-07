from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import traceback
from fastapi import Query
import qrcode
import boto3
import os
import re
from io import BytesIO
from botocore.config import Config


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



# AWS S3 Configuration
s3 = boto3.client(
    "s3",
    region_name="ap-south-1",
    endpoint_url="https://s3.ap-south-1.amazonaws.com",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    config=Config(signature_version="s3v4")
)

bucket_name = 'capstoneprojectdevops' # Add your bucket name here

@app.post("/api/generate-qr/")
async def generate_qr(url: str = Query(...)):
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR Code to BytesIO object
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Generate file name for S3
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', url)
    file_name = f"qr_codes/{safe_name}.png"
    # file_name = f"qr_codes/{url.split('//')[-1]}.png"

    try:
        # Upload to S3
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=img_byte_arr, ContentType='image/png')
        
        # Generate the S3 URL
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': file_name},
            ExpiresIn=3600  # 1 hour    
        )
        print("PRESIGNED URL:", presigned_url)
        return {"qr_code_url": presigned_url}
        # return {"qr_code_url": presigned_url}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    