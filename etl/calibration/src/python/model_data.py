from pandas import DataFrame
from sklearn import neural_network as nn, metrics
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from numpy import nan

from pipe_elements import Filter
import C


def get_pipeline(data):
    fil = Filter(data.to_records(), 1, ['s.co2', 's.no2resistance',
                                  's.o3resistance'],
                 ['secs', 'p.unit.serial.number'])
    ss = StandardScaler()
    mlp = nn.MLPRegressor(solver = 'lbfgs')
    steps = [('filter', fil), ('scale', ss), ('mlp', mlp)]
    pipe = Pipeline(steps)
    return pipe


def optimize_param(pipeline, parameter_grid, x, y):
    gs = RandomizedSearchCV(pipeline, parameter_grid, C.n_iter,
                            n_jobs=C.n_jobs, cv=C.cv_k, verbose=C.verbose,
                            error_score=nan, refit=False)
    gs.fit(x, y)
    return DataFrame.from_dict(gs.cv_results_)


def cv_predictions(pipeline, parameters, x, y):
    pipeline.set_params(**parameters)
    predictions = cross_val_predict(pipeline, x, y, cv=C.cv_k, verbose=3)

    perf = dict()
    perf['r2'] = metrics.r2_score(y, predictions)
    perf['expl_var'] = metrics.explained_variance_score(y, predictions)
    perf['rmse'] = metrics.mean_squared_error(y, predictions)**.5

    return predictions, perf


def learn_final_model(pipeline, parameters, x, y):
    fil = pipeline.named_steps['filter']
    pipeline = Pipeline(pipeline.steps[1:])
    x = fil.transform(x)

    del parameters['filter__alpha']
    pipeline.set_params(**parameters)
    pipeline.fit(x, y)
    return pipeline, fil