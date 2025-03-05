import uvicorn
from fastapi import FastAPI

from app.students.router import router as router_students
from app.major.router import router as router_majors
app = FastAPI()

@app.get("/", summary='Главная страница')
async def home_page():
    return {"message": "Hello World"}

app.include_router(router_students)
app.include_router(router_majors)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")