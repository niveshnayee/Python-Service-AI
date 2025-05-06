import json
import uuid
from model.job_model import JobDescriptionData, StructuredJobDescriptionResponse
from model.resume_model import StructuredResumeResponse, ResumeData
from llm.llm_model import extract_using_llm

def extract_resume_data(text: str) -> StructuredResumeResponse:

    print("Extracting resume data...")
    model_output = extract_using_llm(text, "resume")
    print("returned from LLM")

    try:
        parsed = json.loads(model_output)
        resume_data = ResumeData(**parsed)
        return StructuredResumeResponse(id=str(uuid.uuid4()), data=resume_data)
    except Exception as e:
        print("Raw LLM output:\n", model_output)
        raise ValueError("Failed to parse LLM output into structured format.") from e
    
def extract_job_data(text: str) -> StructuredJobDescriptionResponse:
    """
    This function extracts job description data.
    """

    print("Extracting Job data...")
    model_output = extract_using_llm(text, "job_description")
    print("returned from LLM")

    try:
        parsed = json.loads(model_output)
        job_data = JobDescriptionData(**parsed)
        return StructuredJobDescriptionResponse(data=job_data)
    except Exception as e:
        print("Raw LLM output:\n", model_output)
        raise ValueError("Failed to parse LLM output into structured format.") from e
