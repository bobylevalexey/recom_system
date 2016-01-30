import os

from model import connect
from movielens.get_marks import get_ml_marks
from movielens.get_features import get_users_features, get_movies_features
from regressions import FeaturesToSvd
from movielens.config import ML_DATA_DIR, RSVD_OPTIONS
from svd_model import DictModel
from rsvd import RSVD

if __name__ == "__main__":
    connect()
    ml_model = DictModel()
    ml_model.load(os.path.join(ML_DATA_DIR, 'model.json'))
    u_features = get_users_features()
    m_features = get_movies_features()

    marks = get_ml_marks()

    u_trainer = FeaturesToSvd(ml_model.factors_num)
    m_trainer = FeaturesToSvd(ml_model.factors_num)
    print u_trainer.train(u_features, ml_model.U_matr)
    print u_trainer.train(m_features, ml_model.V_matr)

    new_U = u_trainer.get_vect_dict(u_features)
    new_V = u_trainer.get_vect_dict(m_features)
    new_model = DictModel(ml_model.factors_num, new_U, new_V)

    rsvd_trainer = RSVD(**RSVD_OPTIONS)
    trained_model = rsvd_trainer.train(new_model, marks)

    print ml_model.calc_rmse(marks)
    print new_model.calc_rmse(marks)
    print trained_model.calc_rmse(marks)

