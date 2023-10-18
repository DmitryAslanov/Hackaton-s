from model import Model
from keras.models import load_model
import numpy as np

class PredictAll:

    def __init__(self) -> None:
        pass

    
    def __call__(self, data):
        model_mean = Model.load_model_mean()
        matrix1 = model_mean.predict(data)

        model_quantile_01 = Model.load_model_quantile_01()
        matrix2 = model_quantile_01.predict(data)

        model_quantile_025 = Model.load_model_quantile_025()
        matrix3 = model_quantile_025.predict(data)

        model_quantile_05 = Model.load_model_quantile_05()
        matrix4 = model_quantile_05.predict(data)

        model_quantile_075 = Model.load_model_quantile_075()
        matrix5 = model_quantile_075.predict(data)

        model_quantile_09 = Model.load_model_quantile_09()
        matrix6 = model_quantile_09.predict(data)
        combined_matrix = np.stack([matrix1, matrix2, matrix3, matrix4, matrix5, matrix6], axis=2)
        return combined_matrix
