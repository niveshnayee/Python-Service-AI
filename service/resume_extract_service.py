import json
import uuid
from model.resume_model import StructuredResumeResponse, ResumeData
from llm.resume_model import extract_using_llm

def extract_resume_data(text: str) -> StructuredResumeResponse:

    print("Extracting resume data...")
    model_output = extract_using_llm(text)
    print("returned from LLM")

    try:
        parsed = json.loads(model_output)
        resume_data = ResumeData(**parsed)
        return StructuredResumeResponse(id=str(uuid.uuid4()), data=resume_data)
    except Exception as e:
        print("Raw LLM output:\n", model_output)
        raise ValueError("Failed to parse LLM output into structured format.") from e
