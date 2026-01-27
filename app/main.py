from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from predictor import Predictor

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])


@app.post("/predict")
def get_prediction(date: str):
    return Predictor().predict(date)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)