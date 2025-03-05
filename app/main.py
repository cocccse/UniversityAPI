import uvicorn
from fastapi import FastAPI

from app.students.router import router as router_students
app = FastAPI()

@app.get("/")
async def home_page():
    return {"message": "Hello World"}

app.include_router(router_students)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")