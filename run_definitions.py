
from pymoo.factory import get_termination
import numpy as np


### DEFAULT VALUES ###

### Epidemic model ###

ksi_base_default = 0
A_rel_default = 0.5
r_AP_default = 0
r_U_default = 0.10
r_P_default = 0.0
r_N_default = 0.98
d_vaccine_default = 800*14 # this is in _time steps_, not in days (days would be better)
rel_rho_default = 1.0
delta_param_default = 5
omegaR_param_default = 14
pii_D_default = 0.01
R_0_default = 2.5
rel_lambda_param_default = 0.5
gamma_param_default = 180.0
initial_infect_default = 300
daily_testing_rate_default = 0.0
testing_sensitivity_default = 1.0
testing_specificity_default = 1.0
tau_TT_daily_default = 0.0
eta_default = 0.0
unknown_q_rate_default = 0.0
recovered_q_rate_default = 0.0
negative_q_rate_default = 0.0
positive_q_rate_default = 0.999
testing_cost_default = 100

def get_runs_definitions():

    # runs are defined below as modifications to the default parameter values. If parameter name is not mentioned
    # in the run definition, its default value will be used. Default values are defined in Covid_Run_Optimizer.py
    # (and possibly separately elsewhere, like in visualizations).

    runs = {}

    runs['base_case_no_control']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'lockdown_policy_control_days': "NA",   # no adjustments to testing policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'termination': get_termination("n_gen",1) # no optimization really...
    }

    runs['base_case_no_control_R0_4.0']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'lockdown_policy_control_days': "NA",   # no adjustments to testing policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'R_0': 4.0,
        'termination': get_termination("n_gen",1) # no optimization really...
    }
    ### ROMER CASE SCENARIOS ###
    #------------------------------------------#

    runs['romer']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': []
    }

    runs['romer_no_limit']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_policy_upper_limits': list(0.05 * np.ones(15)),
        'max_daily_tests': 340000000,
    }

    runs['romer_terminal_0.25']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'T_rec': 0.25
    }

    runs['romer_terminal_1.0']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'T_rec': 1.0
    }

    #------------------------------------------#

    runs['romer_R0_4.0']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'R_0': 4.0, # set R0 to a higher value
    }

    runs['romer_R0_4.0_no_limit']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'R_0': 4.0, # set R0 to a higher value
        'max_daily_tests': 340000000,
    }

    runs['romer_R0_1.25']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'R_0': 1.25, # set R0 to a lower value
    }

    # #------------------------------------------#

    runs['romer_R0_4.0_sens_spec_075']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_sensitivity': 0.75,
        'testing_specificity': 0.75,
        'R_0': 4.0, # set R0 to a higher value
    }


    runs['romer_R0_4.0_sens_spec_085']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_sensitivity': 0.85,
        'testing_specificity': 0.85,
        'R_0': 4.0, # set R0 to a higher value
    }

    runs['romer_R0_4.0_sens_spec_090']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_sensitivity': 0.90,
        'testing_specificity': 0.90,
        'R_0': 4.0, # set R0 to a higher value
    }

    runs['romer_R0_4.0_sens_spec_095']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_sensitivity': 0.95,
        'testing_specificity': 0.95,
        'R_0': 4.0, # set R0 to a higher value
    }
    #------------------------------------------#

    runs['romer_6d_incubation']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'delta_param': 6
    }

    runs['romer_6d_incubation_sens_spec_090']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'delta_param': 6,
        'testing_sensitivity': 0.90,
        'testing_specificity': 0.90
    }

    #------------------------------------------#

    runs['romer_8d_incubation']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'delta_param': 8
    }

    #------------------------------------------#

    runs['romer_8d_incubation_sens_spec_075']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'delta_param': 8,
        'testing_sensitivity': 0.75,
        'testing_specificity': 0.75
    }

    #------------------------------------------#

    runs['romer_8d_incubation_sens_spec_090']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'delta_param': 8,
        'testing_sensitivity': 0.90,
        'testing_specificity': 0.90
    }


    runs['romer_3d_delay']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_policy_control_days': [3, 15, 30, 60, 90, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600],
    }


    runs['romer_7d_delay']={    # NOT VERY INFORMATIVE...
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_policy_control_days': [7, 15, 30, 60, 90, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600],
    }


    runs['romer_14d_delay']={   # NOT VERY INFORMATIVE...
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_policy_control_days': [14, 15, 30, 60, 90, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600],
    }

    runs['romer_28d_delay']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_policy_control_days': [28, 29, 30, 60, 90, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600],
    }

    runs['romer_sens_085']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_sensitivity': 0.85,
    }

    runs['romer_spec_085']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_specificity': 0.85,
    }


    #------------------------------------------#

    runs['romer_sens_spec_085']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_sensitivity': 0.85,
        'testing_specificity': 0.85,
    }

    #------------------------------------------#

    runs['romer_sens_spec_090']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_sensitivity': 0.90,
        'testing_specificity': 0.90,
    }

    #------------------------------------------#

    runs['romer_sens_spec_095']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_sensitivity': 0.95,
        'testing_specificity': 0.95,
    }

    runs['romer_sens_spec_098']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_sensitivity': 0.98,
        'testing_specificity': 0.98,
    }

    runs['romer_sens_spec_099']={
        'lockdown_policy_control_days': "NA",   # no adjustments to lockdown policy
        'lockdown_policy_lower_limits': [],
        'lockdown_policy_upper_limits': [],
        'testing_sensitivity': 0.99,
        'testing_specificity': 0.99,
    }

    #------------------------------------------#


    ### LOCKDOWN OPTIMIZATION CASE SCENARIOS ###

    #------------------------------------------#

    runs['base_case_lockdown_opt']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }

    runs['base_case_lockdown_opt_terminal_0.25']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'T_rec': 0.25
    }

    runs['base_case_lockdown_opt_terminal_1.0']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'T_rec': 1
    }

    #------------------------------------------#

    runs['base_case_lockdown_opt_R0_4.0']={
        'R_0': 4.0,
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }

    #------------------------------------------#

    runs['base_case_lockdown_opt_with_limited_general_testing']={
        'daily_testing_rate': 0.01,
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }

    #------------------------------------------#

    runs['base_case_lockdown_opt_with_limited_imperfect(0.75)_general_testing']={
        'daily_testing_rate': 0.01,
        'testing_sensitivity': 0.75,
        'testing_specificity': 0.75,
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }

    runs['base_case_lockdown_opt_with_limited_sens075_general_testing']={
        'daily_testing_rate': 0.01,
        'testing_sensitivity': 0.75,
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }

    runs['base_case_lockdown_opt_with_limited_spec075_general_testing']={
        'daily_testing_rate': 0.01,
        'testing_specificity': 0.75,
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }

    runs['base_case_lockdown_opt_with_limited_sens090_general_testing']={
        'daily_testing_rate': 0.01,
        'testing_sensitivity': 0.90,
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }

    runs['base_case_lockdown_opt_with_limited_spec090_general_testing']={
        'daily_testing_rate': 0.01,
        'testing_specificity': 0.90,
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }



    runs['base_case_lockdown_opt_with_limited_imperfect(0.85)_general_testing']={
        'daily_testing_rate': 0.01,
        'testing_sensitivity': 0.85,
        'testing_specificity': 0.85,
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }
    runs['base_case_lockdown_opt_with_limited_imperfect(0.90)_general_testing']={
        'daily_testing_rate': 0.01,
        'testing_sensitivity': 0.90,
        'testing_specificity': 0.90,
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }
    runs['base_case_lockdown_opt_with_limited_imperfect(0.95)_general_testing']={
        'daily_testing_rate': 0.01,
        'testing_sensitivity': 0.95,
        'testing_specificity': 0.95,
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }
    #------------------------------------------#

    runs['base_case_lockdown_opt_3d_delay']={
        'lockdown_policy_control_days': [3, 15, 30, 60, 90, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600],
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }

    runs['base_case_lockdown_opt_7d_delay']={
        'lockdown_policy_control_days': [7, 15, 30, 60, 90, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600],
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }

    runs['base_case_lockdown_opt_14d_delay']={
        'lockdown_policy_control_days': [14, 15, 30, 60, 90, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600],
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }

    runs['base_case_lockdown_opt_28d_delay']={
        'lockdown_policy_control_days': [28, 29, 30, 60, 90, 120, 150, 200, 250, 300, 350, 400, 450, 500, 600],
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': []
    }

    runs['base_case_6d_incubation']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'delta_param': 6,
    }


    runs['base_case_8d_incubation']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'delta_param': 8,
    }

    ##### TEST and TRACE CASES #####


    # Fixed testing rate:
    runs['test_and_trace_lockdown_opt_eta10']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'eta': 0.50,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'max_daily_tests': 340000000
    }

    runs['test_and_trace_lockdown_opt_eta50']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'eta': 0.50,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'max_daily_tests': 340000000
    }

    runs['test_and_trace_lockdown_opt_eta75']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'eta': 0.75,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'max_daily_tests': 340000000

    }

    runs['test_and_trace_lockdown_opt_eta95']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'eta': 0.95,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'max_daily_tests': 340000000
    }


    runs['test_and_trace_lockdown_opt_eta100']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'eta': 1.00,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'max_daily_tests': 340000000
    }

    runs['test_and_trace_lockdown_opt_eta50_R04']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'eta': 0.50,
        'R_0': 4.0,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'max_daily_tests': 340000000
    }
    runs['test_and_trace_lockdown_opt_eta75_R04']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'eta': 0.75,
        'R_0': 4.0,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'max_daily_tests': 340000000
    }

    runs['test_and_trace_lockdown_opt_eta100_R04']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'eta': 1.00,
        'R_0': 4.0,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'max_daily_tests': 340000000
    }

    runs['test_and_trace_lockdown_opt_eta50_R04_delta10']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'eta': 0.50,
        'R_0': 4.0,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'max_daily_tests': 340000000,
        'delta_param': 10
    }

    runs['test_and_trace_lockdown_opt_eta75_R04_delta10']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'eta': 0.75,
        'R_0': 4.0,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'max_daily_tests': 340000000,
        'delta_param': 10
    }


    runs['test_and_trace_lockdown_opt_eta100_R04_delta10']={
        'testing_policy_control_days': "NA",   # no adjustments to testing policy
        'testing_policy_lower_limits': [],
        'testing_policy_upper_limits': [],
        'eta': 1.00,
        'R_0': 4.0,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'max_daily_tests': 340000000,
        'delta_param': 10
    }

     #------- COMBO STRATEGIES ------- #

    runs['combo_base_case']={
    }

    runs['combo_base_case_R0_4.0'] = {
        'R_0': 4.0,
    }

    runs['combo_base_case_test_and_trace'] = {
        'eta': 1.00,
        'tau_TT_daily': 0.5,
        'r_U': 0.01,
        'delta_param': 10
    }

    runs['combo_sens_spec_0.95'] = {
        'testing_sensitivity': 0.95,
        'testing_specificity': 0.95,
    }

    runs['combo_sens_spec_0.85'] = {
        'testing_sensitivity': 0.85,
        'testing_specificity': 0.85,
    }

    runs['combo_R0_4.0_sens_spec_0.95'] = {
        'R_0': 4.0,
        'testing_sensitivity': 0.95,
        'testing_specificity': 0.95,
    }

    runs['combo_R0_4.0_sens_spec_0.85'] = {
        'R_0': 4.0,
        'testing_sensitivity': 0.85,
        'testing_specificity': 0.85,
    }

    return runs