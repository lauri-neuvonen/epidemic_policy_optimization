# This script is used to run different optimization cases for different epidemic scenarios. It is a batch run compatible
# ...version of the notebook 'Covid_Policy_Optimization.ipynb'

# If run from command line, requires 2 arguments: number of max generations and list of runs to optimize for NSGA-II

# Dictionaries to hold run data and results:


import sys

import numpy as np
from pymoo.util.misc import stack
from pymoo.model.problem import Problem
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.performance_indicator.hv import Hypervolume
from pymoo.util.termination.default import MultiObjectiveDefaultTermination
from pymoo.model.evaluator import Evaluator

from pymoo.factory import get_termination
from pymoo.optimize import minimize
# from pymoo.visualization.scatter import Scatter
from policy_epidemic_model_code import *
from run_tools import create_epidemic_model, Policy
# import importlib
# import matplotlib.pyplot as plt

import pandas as pd
import argparse
from run_definitions import *

parser = argparse.ArgumentParser(description='Run optimization run using an NSGA-II algorithm for COVID-19 simulator')
parser.add_argument('max_gen', type=int, help='maximum number of generations for NSGA-II algorithm.')
parser.add_argument('runs', type=str, nargs='+', help='dictionary of run values to be changed from defaults')

args = parser.parse_args()

epidemic_simulators = {}
result_dataframes = {}
objective_dataframes = {}
constraint_dataframes = {}
problems = {}

### RUN SETTINGS ###

max_gen = args.max_gen # 1000 # set low for testing, high for proper optimization runs. By default, optimization terminates
                    # ...when convergence has been observed or this limit of iterations reached.

# Tools for building optimization runs based on params.

arg_runs = args.runs # dictionary to hold all runs
print("Will optimize: ", arg_runs)

runs = get_runs_definitions()

#### OPTIMIZATION ENGINE ###
# MODIFY ONLY IF YOU KNOW WHAT YOU'RE _DOING
# Modifications here affect how the optimizer works, not run definitions

class COVID_policy(Problem):

    def __init__(self, model, model_case, lockdown_policy_control_days, lockdown_policy_lower_limits,
                 lockdown_policy_upper_limits, testing_policy_control_days, testing_policy_lower_limits,
                 testing_policy_upper_limits, max_daily_tests, p_ICU, C_hos, T_rec):
        self.model = model
        self.model_case = model_case
        self.max_daily_tests_lim = max_daily_tests
        self.testing_policy_control_days = testing_policy_control_days
        self.lockdown_policy_control_days = lockdown_policy_control_days
        self.p_ICU = p_ICU
        self.C_hos = C_hos
        self.T_rec = T_rec

        if lockdown_policy_control_days == "NA":
            self.n_var_ld = 0
            self.lockdown_policy_control_days = []
            self.lockdown_policy_lower_limits = []
            self.lockdown_policy_upper_limits = []
        else:
            self.n_var_ld = len(lockdown_policy_control_days)
            self.lockdown_policy_upper_limits = lockdown_policy_upper_limits
            self.lockdown_policy_lower_limits = lockdown_policy_lower_limits

        if testing_policy_control_days == "NA":
            self.n_var_t = 0
            self.testing_policy_lower_limits = []
            self.testing_policy_upper_limits = []
        else:
            self.n_var_t = len(testing_policy_control_days)
            self.testing_policy_lower_limits = testing_policy_lower_limits
            self.testing_policy_upper_limits = testing_policy_upper_limits


        super().__init__(n_var=self.n_var_ld+self.n_var_t,
                         n_obj=3,
                         n_constr=1,
                         xl=np.array(self.lockdown_policy_lower_limits + self.testing_policy_lower_limits),
                         xu=np.array(self.lockdown_policy_upper_limits + self.testing_policy_upper_limits)
        )

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = []     # holds first objective
        f2 = []     # holds second objective...
        f3 = []

        g1 = []     # holds first constraint

        for j in range(len(x[:, 1])):  # evaluate f1 and f2 for each individual

            # these slices contain indexing for decision variables representing lockdown and testing:
            lockdown_var_slice = slice(0, self.n_var_ld + 1)
            testing_var_slice = slice(self.n_var_ld,
                                      self.n_var_ld + self.n_var_t + 1)

            # create policies (dictionaries) for lockdown and testing
            lockdown_policy = create_sub_policy(self.lockdown_policy_control_days, x[j, lockdown_var_slice])
            testing_policy = create_sub_policy(self.testing_policy_control_days, x[j, testing_var_slice])
            policy = Policy(lockdown_policy, testing_policy)

            Reported_D, Notinfected_D, Unreported_D, Infected_D, \
            False_pos, False_neg, Recovered_D, Dead_D, Infected_T, Infected_not_Q, Infected_in_Q, Y_D, M_t, Y_total, total_testing_cost, tests, Unk_NA_nQ_D, Unk_NA_Q_D, K_NA_nQ_D, Unk_IA_nQ_D, Unk_IA_Q_D, K_IA_Q_D, alpha_D, ksi_TT_I_D, ksi_TT_N_D, ksi_TT_R_D, Symptomatic_T \
                = self.model.solve_case(self.model_case, policy)

            T_rec_t = int(round(14 * 365 * self.T_rec)) # change from years to time steps
            #Costs:
            cost_e = -Y_total / self.model.T # contains loss of output & scaled direct costs
            cost_terminal = ((T_rec_t) / 2) * (-Y_D[-1]) / self.model.T
            deaths_terminal = ((T_rec_t) / 2) * ((Dead_D[-1]-Dead_D[-2]) * self.model.pop / 1000) / self.model.T # Deaths are cumulative, so difference needed for current rate
            hcap_terminal = ((T_rec_t) / 2) * np.max([0.0, self.p_ICU * Symptomatic_T[-1] - self.C_hos / self.model.pop])
            #print("cost_e: ", cost_e)
            #print("cost_terminal: ", cost_terminal)

            # objectives scaled to roughly same scale
            f1.append(Dead_D[-1] * self.model.pop / 1000 + deaths_terminal)
            f2.append(cost_e + cost_terminal)
            f3.append(np.max([0.0, self.p_ICU * max(Symptomatic_T) - self.C_hos / self.model.pop]) + hcap_terminal)  # algorithm minimizes peak symptomatics

            max_daily_tests_value = max(tests)

            g1_val = (max_daily_tests_value - self.max_daily_tests_lim)/self.max_daily_tests_lim
            g1.append(g1_val)     # constraints set in g(x) <= 0 format, normalized per coefficients

        out["F"] = np.column_stack([f1, f2, f3])
        out["G"] = np.column_stack([g1])



def create_sub_policy(policy_control_times, policy_control_values):
    policy = {}  # this will hold the policy in format suitable for input to the epidemic model
    if policy_control_times == "NA":
        return "NA"
    else:
        for (i, t) in enumerate(policy_control_times):
            policy[t] = policy_control_values[i]

        return policy

def create_policy(lockdown_policy, testing_policy):

    return Policy(lockdown_policy, testing_policy)

# Run generator
def create_optimization_run(
               pop_size=60,
               n_offsprings=30,
               sampling=get_sampling("real_random"),
               crossover=get_crossover("real_sbx", prob=0.9, eta=10),
               mutation=get_mutation("real_pm", eta=8),
               eliminate_duplicates=True,
               filename="foo",
               # termination = get_termination("n_gen",50),
               termination=MultiObjectiveDefaultTermination(
                   x_tol=1e-8,
                   cv_tol=1e-6,
                   f_tol=0.0025,
                   nth_gen=5,
                   n_last=30,
                   n_max_gen=max_gen,
                   n_max_evals=100000,
               ),

               lockdown_policy_control_days=[1, 15, 30, 60, 90, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600],
               lockdown_policy_lower_limits=list(0.5 * np.ones(15)),  # can't use len(l_p_c_d) within function param def
               lockdown_policy_upper_limits=list(1.0 * np.ones(15)),  # needs to be different from lower limit
               testing_policy_control_days=[1, 15, 30, 60, 90, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600],
               testing_policy_lower_limits=list(np.zeros(15)),
               testing_policy_upper_limits=list(0.02 * np.ones(15)),
               max_daily_tests=10_000_000,
                p_ICU=0.01,
               C_hos=100000,
               T_rec=0.5, # recovery time in years from end of experiment
                **epidemic_model_params
               ):

    model, model_case = create_epidemic_model(**epidemic_model_params)

    #print("DEBUG policy parameters:")
    #print("ld days:", lockdown_policy_control_days)
    #print("ld lolim: ", lockdown_policy_lower_limits)
    #print("ld hilim:", lockdown_policy_upper_limits)
    #print("t days:", testing_policy_control_days)
    #print("t lolim: ", testing_policy_lower_limits)
    #print("t hilim:", testing_policy_upper_limits)

    problem = COVID_policy(model, model_case, lockdown_policy_control_days, lockdown_policy_lower_limits,
                           lockdown_policy_upper_limits, testing_policy_control_days, testing_policy_lower_limits,
                           testing_policy_upper_limits, max_daily_tests, p_ICU, C_hos, T_rec)

    # create initial population here

    initial_pop_x = get_sampling("real_random") # random sampling for first population

    algorithm = NSGA2(
        pop_size=pop_size,
        n_offsprings=n_offsprings,
        sampling=initial_pop_x,
        crossover=crossover,
        mutation=mutation,
        eliminate_duplicates=True
    )

    return problem, algorithm, termination, model, model_case



# NOTE: default values for all adjustable run parameters defined in function definition below:


# loop through the different runs and
for run in arg_runs:
    problem, algorithm, termination, model, model_case = create_optimization_run(**runs[run])
    epidemic_simulators[run] = (model, model_case)
    problems[run] = problem

    print("Optimizing run ", run)
    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=1,
                   # pf=problem.pareto_front(use_cache=False),
                   save_history=False,  # True Needed for convergence analysis
                   verbose=True)

    # Which one to use? Pandas makes it easier to save column names...
    # np.savetxt('results/'+run+'_results.csv', res.X, delimiter=",")
    # np.savetxt('results/'+run+'_objectives.csv', res.F, delimiter=",")

    if (problem.lockdown_policy_control_days != "NA") & (problem.testing_policy_control_days != "NA"):
        df_column_names = problem.lockdown_policy_control_days + problem.testing_policy_control_days
    elif problem.lockdown_policy_control_days != "NA":
        df_column_names = problem.lockdown_policy_control_days
    else:
        df_column_names = problem.testing_policy_control_days

    res_df = pd.DataFrame(data=res.X,
                          columns=df_column_names)
    res_df.to_csv('results/' + run + '_results.csv', index=False)
    result_dataframes[run] = res_df

    obj_df = pd.DataFrame(data=res.F, columns=['Deaths', 'Economic impact', 'Peak Symptomatics'])
    obj_df.to_csv('results/' + run + '_objectives.csv', index=False)
    objective_dataframes[run] = obj_df

    constr_df = pd.DataFrame(data=res.G, columns=['Max daily tests marginal'])
    constr_df.to_csv('results/' + run + '_constraints.csv', index=False)
    constraint_dataframes[run] = constr_df



print("Runs completed and results saved")

