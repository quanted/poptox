import numpy as np
import os.path
import pandas as pd
import sys
#find parent directory and import base (travis)
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from base.uber_model import UberModel, ModelSharedInputs

#print(sys.path)
#print(os.path)

class FoxsurplusInputs(ModelSharedInputs):
    """
    Input class for Foxsurplus.
    #(N_o,K,rho,q,E,T)
    """

    def __init__(self):
        """Class representing the inputs for Foxsurplus"""
        super(FoxsurplusInputs, self).__init__()
        self.init_pop_size = pd.Series([], dtype="float")
        self.growth_rate = pd.Series([], dtype="float")
        self.time_steps = pd.Series([], dtype="float")
        self.carrying_capacity = pd.Series([], dtype="float")
        self.catchability = pd.Series([], dtype="float")
        self.effort = pd.Series([], dtype="float")


class FoxsurplusOutputs(object):
    """
    Output class for Foxsurplus.
    """

    def __init__(self):
        """Class representing the outputs for Foxsurplus"""
        super(FoxsurplusOutputs, self).__init__()
        self.out_pop_time_series = pd.Series(name="out_pop_time_series")


class Foxsurplus(UberModel, FoxsurplusInputs, FoxsurplusOutputs):
    """
    Foxsurplus model for population growth.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Foxsurplus model and containing all its methods"""
        super(Foxsurplus, self).__init__()
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        self.pd_obj_out = None

    def execute_model(self):
        """
        Callable to execute the running of the model:
            1) Populate input parameters
            2) Create output DataFrame to hold the model outputs
            3) Run the model's methods to generate outputs
            4) Fill the output DataFrame with the generated model outputs
        """
        self.populate_inputs(self.pd_obj, self)
        self.pd_obj_out = self.populate_outputs(self)
        self.run_methods()
        self.fill_output_dataframe(self)

    # Begin model methods
    def run_methods(self):
        """ Execute all algorithm methods for model logic """
        try:
            self.Foxsurplus_growth()
        except Exception as e:
            print(str(e))

    def foxsurplus_growth(self):
        T=self.time_steps
        index_set = range(T+1)
        x = np.zeros(len(index_set))
        x[0] = self.init_pop_size
        K = self.carrying_capacity
        rho=self.growth_rate/100
        q=self.catchability
        E=self.effort
        for n in index_set[1:]:
            x[n] = np.exp((rho*np.log(K)-E*q+((E*q-rho*np.log(K)+rho*np.log(N_o))/np.exp(rho*n)))/rho)
        x=x.tolist()
        return x