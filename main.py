import time
from fastapi import FastAPI, HTTPException, Header, Depends
from model.job_model import JobRequest, StructuredJobDescriptionResponse
from model.resume_model import ResumeRequest, StructuredResumeResponse
from service.resume_extract_service import extract_job_data, extract_resume_data
import os
import jwt  
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

app = FastAPI()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")  
ALGORITHM = os.getenv("ALGORITHM")  # The algorithm used to sign the JWT


async def verify_token(authorization: str = Header(...), service_name: str = Header(...)):
   try:
        # Extract the token from the Authorization header
        token = authorization.split(" ")[-1]  # "Bearer <token>"

        # Decode the JWT token using the secret key and algorithm
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the service name (subject) from the decoded token
        token_service_name = decoded_token.get("sub")  # 'sub' is the service name
        print(f"Token service name: {token_service_name}")
        # Verify that the service name in the token matches the service name in the header
        if token_service_name != service_name:
            raise HTTPException(status_code=401, detail="Unauthorized: Service name mismatch")
        
        # Optionally, check the expiration of the token
        if decoded_token.get("exp") < int(time.time()):
            raise HTTPException(status_code=401, detail="Token has expired")
        

   except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
   except jwt.InvalidTokenError:
        print("Invalid token error")
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/extract-resume", response_model=StructuredResumeResponse)
def extract_resume(req: ResumeRequest,  _: None = Depends(verify_token)):
    print("Received request to extract resume data...")
    return extract_resume_data(req.text)


@app.post("/extract-job", response_model=StructuredJobDescriptionResponse)
def extract_resume(req: JobRequest,  _: None = Depends(verify_token)):
    print("Received request to extract job data...")
    return extract_job_data(req.text)