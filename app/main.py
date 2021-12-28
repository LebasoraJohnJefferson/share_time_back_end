from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import user,auth,store

app = FastAPI()

origins=["http://localhost:8000","http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def Introduction():
    return {'message':'welcome to my api'}

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(store.router)


