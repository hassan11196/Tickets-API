import numpy as np
import pandas as pd
import os
from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, APIRouter
from pydantic import BaseModel, ValidationError, validator
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .api.endpoints.ticket import router as ticket_router
from .db.mongodb_utils import close_mongo_connection, connect_to_mongo
router = APIRouter()
router.include_router(ticket_router)


# from .ml.model import Model, get_model, n_features

# class PredictRequest(BaseModel):
#     data: List[List[float]]

#     @validator("data")
#     def check_dimensionality(cls, v):
#         for point in v:
#             if len(point) != n_features:
#                 raise ValueError(f"Each data point must contain {n_features} features")

#         return v


# class PredictResponse(BaseModel):
#     data: List[float]


app = FastAPI(port=os.environ.get('PORT'), title='FAST API TICKET API')
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)
app.include_router(router)

# @app.get('/')
# def index():
    
#     model = get_model()
#     dat = model.auto_train()
#     model.save()
#     return {'status':'trained', **dat}

# @app.post("/predict", response_model=PredictResponse)
# def predict(input: PredictRequest, model: Model = Depends(get_model)):
#     X = np.array(input.data)

#     y_pred = model.predict(X)
#     result = PredictResponse(data=y_pred.tolist())

#     return result


# @app.post("/predict_csv")
# def predict_csv(csv_file: UploadFile = File(...), model: Model = Depends(get_model)):
#     try:
#         df = pd.read_csv(csv_file.file).astype(float)
#     except:
#         raise HTTPException(
#             status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Unable to process file"
#         )

#     df_n_instances, df_n_features = df.shape
#     if df_n_features != n_features:
#         raise HTTPException(
#             status_code=HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=f"Each data point must contain {n_features} features",
#         )

#     y_pred = model.predict(df.to_numpy().reshape(-1, n_features))
#     result = PredictResponse(data=y_pred.tolist())

#     return result