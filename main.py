from fastapi import FastAPI, Request, HTTPException, Header, Depends
from model.resume_model import ResumeRequest, StructuredResumeResponse
from service.resume_extract_service import extract_resume_data
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

app = FastAPI()

async def verify_token(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    if token != os.getenv("MICROSERVICE_TOKEN"):
        print("Unauthorized access attempt detected.")
        print(f"Token provided: {token}")
        print(f"Expected token: {os.getenv('MICROSERVICE_TOKEN')}")
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/extract-resume", response_model=StructuredResumeResponse)
def extract_resume(req: ResumeRequest,  _: None = Depends(verify_token)):
    print("Received request to extract resume data...")
    return extract_resume_data(req.text)
