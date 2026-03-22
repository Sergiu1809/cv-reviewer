from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = anthropic.Anthropic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Resume(BaseModel):
    resume_text: str


@app.post("/review")
def review_cv(resume: Resume):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": resume.resume_text}],
        system="You are a CV reviewer. Structure your feedback in clear sections: overall impression, strengths, weaknesses, suggestions. Be an honest reviewer and return an honest review.",
    )
    return {"response": response.content[0].text}


# anything that isn't an API route -> look for it in the static/ folder
app.mount("/", StaticFiles(directory="static", html=True), name="static")
