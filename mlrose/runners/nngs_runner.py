from mlrose import NNClassifier
from mlrose.decorators import short_name
from mlrose.runners._nn_runner_base import _NNRunnerBase
from mlrose.decorators import get_short_name

"""
Example usage:
    from mlrose.runners import NNGSRunner

    grid_search_parameters = ({
        'max_iters': [1, 2, 4, 8, 16, 32, 64, 128],                     # nn params
        'learning_rate': [0.001, 0.002, 0.003],                         # nn params
        'schedule': [ArithDecay(1), ArithDecay(100), ArithDecay(1000)]  # sa params
    })

    nnr = NNGSRunner(x_train=x_train,
                     y_train=y_train,
                     x_test=x_test,
                     y_test=y_test,
                     experiment_name='nn_test',
                     algorithm=mlrose.algorithms.sa.simulated_annealing,
                     grid_search_parameters=grid_search_parameters,
                     iteration_list=[1, 10, 50, 100, 250, 500, 1000, 2500, 5000, 10000],
                     bias=True,
                     early_stopping=False,
                     clip_max=1e+10,
                     max_attempts=500,
                     generate_curves=True,
                     seed=200972)

    results = nnr.run()          # GridSearchCV instance returned    
"""


@short_name('nngs')
class NNGSRunner(_NNRunnerBase):

    def __init__(self, x_train, y_train, x_test, y_test, experiment_name, seed, iteration_list, algorithm,
                 grid_search_parameters, bias=True, early_stopping=False, clip_max=1e+10,
                 max_attempts=500, generate_curves=True, output_directory=None):

        # update short name based on algorithm
        self._set_dynamic_runner_name(f'{get_short_name(self)}_{get_short_name(algorithm)}')

        # call base class init
        super().__init__(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test,
                         experiment_name=experiment_name,
                         seed=seed,
                         iteration_list=iteration_list,
                         grid_search_parameters=grid_search_parameters,
                         generate_curves=generate_curves,
                         output_directory=output_directory)

        # build the classifier
        self.classifier = NNClassifier(runner=self,
                                       algorithm=algorithm,
                                       max_attempts=max_attempts,
                                       clip_max=clip_max,
                                       early_stopping=early_stopping,
                                       bias=bias)

    def run_one_experiment_(self, algorithm, total_args, **params):
        if self._extra_args is not None and len(self._extra_args) > 0:
            params = {**params, **self._extra_args}

        total_args.update(params)
        total_args.pop('problem')
        user_info = [(k, v) for k, v in total_args.items()]

        return self._invoke_algorithm(algorithm=algorithm,
                                      curve=self.generate_curves,
                                      user_info=user_info,
                                      additional_algorithm_args=total_args,
                                      **params)

