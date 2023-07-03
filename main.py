from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import tiktoken
import os

load_dotenv()
oauth2_token = os.getenv("OAUTH2_TOKEN")

class Item(BaseModel):
    text: str

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/count-tokens")
def count_tokens(item: Item, token: str = Depends(oauth2_scheme)):
    if token != oauth2_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = len(encoding.encode(item.text))
    return { "tokens" : tokens }

