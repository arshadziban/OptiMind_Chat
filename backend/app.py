from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi.middleware.cors import CORSMiddleware
import torch
import os

# -----------------------------------------------------------
# FastAPI Application Configuration
# -----------------------------------------------------------
app = FastAPI(
    title="Book Chatbot API",
    description="API for generating responses from the fine-tuned Book Chatbot model.",
    version="1.0.0"
)

# -----------------------------------------------------------
# CORS Configuration
# -----------------------------------------------------------
origins = [
    "http://localhost:3000",            # Local React frontend
    "https://your-frontend-domain.com"  # Replace with deployed frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------
# Model Loading (Local Path)
# -----------------------------------------------------------
MODEL_PATH =  r"E:/Important/Skills/book_chat_bot/backend/model/book_model"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model path not found: {MODEL_PATH}")

print("Loading model from:", MODEL_PATH)

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    local_files_only=True,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

print("Model loaded successfully.")

# -----------------------------------------------------------
# Request Schema Definition
# -----------------------------------------------------------
class Query(BaseModel):
    prompt: str

# -----------------------------------------------------------
# Text Generation Endpoint
# -----------------------------------------------------------
@app.post("/generate")
async def generate_text(data: Query):
    """
    Generate a response based on the input prompt using the fine-tuned model.
    """
    full_prompt = f"""Below is a question related to the book.

### Instruction:
{data.prompt}

### Response:
"""

    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)

    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=600,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id
        )

    reply = tokenizer.decode(output[0], skip_special_tokens=True)
    response = reply.split("### Response:")[-1].strip()

    print("\n--- User Prompt ---")
    print(data.prompt)
    print("\n--- Model Response ---")
    print(response)
    print("--------------------------\n")

    return {"response": response}

# -----------------------------------------------------------
# Health Check Endpoints
# -----------------------------------------------------------
@app.get("/")
async def root():
    return {"message": "Book Chatbot API is running successfully."}

@app.get("/ping")
async def ping():
    return {"message": "pong"}

# -----------------------------------------------------------
# Run Command
# -----------------------------------------------------------
# Use the following command to run the API:
# uvicorn app:app --reload
# -----------------------------------------------------------
