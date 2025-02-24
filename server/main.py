from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run

from server.router import routerTrain, routerPred
from us_visa.constants import APP_HOST, APP_PORT


# Initialize fastapi client
app = FastAPI()

# declare default middlewares
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    try:
        return {"Health_Check_Status": "OK", "Connection": "Alive"}

    except Exception as e:
        raise Exception(f"Error starting http server : {e}")

# routers
app.include_router(routerTrain)
app.include_router(routerPred)

if __name__ == "__main__":
    app_run(app=app, host=APP_HOST, port=APP_PORT)
