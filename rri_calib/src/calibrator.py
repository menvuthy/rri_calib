import os
import glob
import spotpy
import subprocess
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from typing import Dict, List, Sequence, Tuple, Optional
import spotpy
from dataclasses import dataclass
from pathlib import Path

import warnings
warnings.filterwarnings('ignore')


@dataclass(frozen=True)
class RRIPaths:
    # base directory
    base_dir: Path = Path(".")
    calInput: Path = Path("rri_calib/ParameterSetting.xlsx")
    rri_input: Path = Path("RRI_Input.txt")

        '''
        The code was hidden for commercial use. Please contact the author for more details.
        '''
        
    # exe files
    rri_exe: Path = Path("0_rri_1_4_2_6.exe")
    calcHydro_exe: Path = Path("calcHydro.exe")
    
class CalibrateRRI:
   
    def __init__(self, paths: RRIPaths = RRIPaths()):
        # Make input/output directory exist at start
        self.paths = paths
        self.paths.plot_dir.mkdir(parents=True, exist_ok=True)
        
        # Read parameter ranges and create SpotPy parameter objects
        self.params = self.read_parameter_setting(self.paths.calInput)

        '''
        The code was hidden for commercial use. Please contact the author for more details.
        '''

        # Cache observed data once (faster)
        self.obs_disc = self._read_obs_all()

    def read_parameter_setting(self, file_path: Path):
        # Load parameter file
        df = pd.read_excel(file_path)

        '''
        The code was hidden for commercial use. Please contact the author for more details.
        '''
        
        return params_list
    
    def read_iteration(self):
        '''
        The code was hidden for commercial use. Please contact the author for more details.
        '''
        return iteration
    
    def calibration_log(self):
        calLog = 'rri_calib/out/calibration_log'
        return calLog
    
    # ---------- Reading discharge ----------
    def _read_obs_all(self) -> List[pd.Series]:
        '''
        The code was hidden for commercial use. Please contact the author for more details.
        '''
        return obs_list
    

    # Function to generate parameters
    def parameters(self):
        '''
        The code was hidden for commercial use. Please contact the author for more details.
        '''
        return params
    

    # ---------- Updating RRI input files ----------
    def update_inputs(self, vector):
        with open(self.paths.rri_input, 'r') as file:
            lines = file.readlines()
            
        '''
        The code was hidden for commercial use. Please contact the author for more details.
        '''

        with open(self.paths.rri_input, 'w') as file:
            file.writelines(lines)

    def _run_exe(self, exe_path: Path) -> None:
        if not exe_path.exists():
            raise FileNotFoundError(f"Missing executable: {exe_path}")
        subprocess.run([str(exe_path)], check=True)
               
    def read_sim(self):
        sim_path = pd.read_csv(self.paths.sim_dir, header=None).loc[2].item()

        sim_discharge_list = []

        '''
        The code was hidden for commercial use. Please contact the author for more details.
        '''

        return sim_discharge_list
    
    def simulation(self, vector):
        '''
        The code was hidden for commercial use. Please contact the author for more details.
        '''

        return self.read_sim()
    
    def evaluation(self):
        return self.obs_disc

    def objectivefunction(self, simulation, evaluation):
        # Read input objective function
        df = pd.read_excel(self.paths.calInput)
        objFun = df.iloc[4, 3]
       
        rmse_list = []
        mae_list = []
        r2_list = []

        '''
        The code was hidden for commercial use. Please contact the author for more details.
        '''

        # Average metrics across all stations
        avg_rmse = np.mean(rmse_list)
        avg_mae = np.mean(mae_list)

        
        
        # Return metrics
        if objFun == "RMSE":
            '''
            The code was hidden for commercial use. Please contact the author for more details.
            '''
            return avg_rmse
        else:
            '''
            The code was hidden for commercial use. Please contact the author for more details.
            '''
            return avg_mae

        
    # ---------- Plot ----------
    def plot_hydro(
        self,
        sim_list: Sequence[pd.Series],
        obs_list: Sequence[pd.Series],
        objfunc: float
    ) -> None:
        self.paths.plot_dir.mkdir(exist_ok=True)

        '''
        The code was hidden for commercial use. Please contact the author for more details.
        '''

        return

        