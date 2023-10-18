from fastapi import FastAPI, APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd
import numpy as np
from predict_all import PredictAll

app = FastAPI()
just_do_it = PredictAll()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):

    x = np.load(file.file)
    result = just_do_it(x)


    response = StreamingResponse(iter([np.save('prediction', result)]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=prediction.csv"
    return response