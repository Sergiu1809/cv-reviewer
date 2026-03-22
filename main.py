from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import anthropic
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = anthropic.Anthropic()


class Resume(BaseModel):
    resume_text: str


@app.post("/review")
def review_cv(resume: Resume):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": resume.resume_text}],
        system="You are a CV/resume reviewer. Structure your feedback in clear sections: overall impression, strengths, weaknesses, suggestions. Be an honest reviewer and return an honest review.",
    )
    return {"response": response.content[0].text}


# anything that isn't an API route -> look for it in the static/ folder
app.mount("/", StaticFiles(directory="static", html=True), name="static")
