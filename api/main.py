from fastapi import FastAPI
from api.routers.statsbomb_routers import router as statsbomb_router

api = FastAPI()
api.include_router(statsbomb_router)

#porta do render é por padrão a 10000

@api.get("/")
def read_root():
    return {"Status": "API is running!"}

#.venv\Scripts\activate    
#uvicorn api.main:api --reload --port 8000
