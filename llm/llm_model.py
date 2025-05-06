import os
import json
from groq import Groq
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def resume_format_prompt(resume_text: str) -> str:
    return f""" 
You are a professional resume parser. Extract structured JSON from this resume.
Return ONLY valid JSON without additional commentary.

Expected JSON schema:
{{
  "full_name": string,
  "email": string,
  "phone": string,
  "address": string,
  "summary": string,
  "skills": [string],
  "education": [{{"degree": string, "institution": string, "start_year": string, "end_year": string}}],
  "experience": [{{"company": string, "title": string, "start_date": "YYYY-MM",, "end_date": "YYYY-MM or Present",
      "duration": "int (months)", "responsibilities": string}}],
  "certifications": [string],
  "projects": [{{"name": string, "description": string, "technologies": [string]}}],
  "languages": [string]
}}

Resume Text:
\"\"\"
{resume_text}
\"\"\"
Only include fields you can confidently extract. 
For missing fields, provide empty strings (`""`) for strings, empty lists (`[]`) for lists, and `0` for integers.

Return valid JSON only which MATCH the Above JSON schema.
"""

def job_format_prompt(description_text: str) -> str:
    return f""" 
You are a professional Job Description parser. Return ONLY valid JSON without additional commentary.
Extract the following information from the job description below and return as a JSON object using these exact keys:

Expected JSON schema:
{{
  "title": "",                  // The main job title (e.g., "Software Engineer")
  "keySkills": [],              // A list of the most important technical or soft skills required (e.g., ["Java", "Spring Boot", "Teamwork"])
  "responsibility": "",         // A Concise&Precise summary of the primary responsibilities for this role
  "requirements": ""            // A Concise&Precise summary of the main requirements or qualifications for candidates
}}

Job Description:
\"\"\"
{description_text}
\"\"\"
Rules:
- Only include information explicitly present in the job description.
- For keySkills, list only the most relevant and specific skills (avoid generic terms like "good communication").
- Do not invent or infer information not in the text.
- If a section is missing, return an empty string or empty list for that field.
Return valid JSON only which MATCH the Above JSON schema.
"""

def extract_using_llm(text: str, service: str) -> str:
    if not GROQ_API_KEY:
        return json.dumps({"error": "GROQ_API_KEY not set in environment variables"})
    

    if service == "resume":
        prompt = resume_format_prompt(text)
    elif service == "job_description":
        prompt = job_format_prompt(text)

    print("extracting with LLm......")
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",  # Use Groq's model
            max_tokens=1024,
            temperature=0.1,
            top_p=0.95,
        )
        
        # Extract the generated text
        generated_text = chat_completion.choices[0].message.content
        
        # Try to parse JSON from the response
        try:
            json_start = generated_text.find("{")
            json_end = generated_text.rfind("}") + 1
            json_str = generated_text[json_start:json_end]
            return json_str
        except Exception as e:
            return json.dumps({
                "error": "Failed to parse JSON from API response",
                "raw_output": generated_text
            })
            
    except Exception as e:
        return json.dumps({
            "error": f"API request failed: {str(e)}"
        })
