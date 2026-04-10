from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Organizational Memory Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins (including your local HTML file)
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, GET, etc.
    allow_headers=["*"],  # Allows all headers
)




app.include_router(router)


@app.get("/")
def root():
    return {"status": "running"}