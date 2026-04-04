import os
import glob
import spotpy
import subprocess
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import proplot
import warnings
warnings.filterwarnings('ignore')
from sklearn.metrics import mean_squared_error, r2_score

from typing import Dict, List, Sequence, Tuple, Optional
import spotpy

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RRIPaths:
    # base directory
    base_dir: Path = Path(".")
    calInput: Path = Path("calibrateRRI/ParameterSetting.xlsx")
    rri_input: Path = Path("RRI_Input.txt")

    # input and output directory
    obs_dir: Path = Path("calibrateRRI/obs")
    sim_dir: Path = Path("calcHydro.txt")
    plot_dir: Path = Path("calibrateRRI/output/plot")
        
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

        # Cache station files once
        df = pd.read_excel(self.paths.calInput)
        obsFile = df.iloc[2, 3]
        self.station_files = sorted([p.name for p in self.paths.obs_dir.glob(obsFile)])

        # Cache observed data once (faster)
        self.obs_disc = self._read_obs_all()

    def read_parameter_setting(self, file_path: Path):
        
        df = pd.read_excel(file_path)

        # Define a list of parameter names
        param_names = df.iloc[7:, 2].values

        # Define a list of optimize values 
        starts = df.iloc[7:, 3].values
        stops = df.iloc[7:, 4].values

        params_list = []
        for i in range(len(param_names)):
            # Create a Uniform parameter with the corresponding name, low, and high values
            param = spotpy.parameter.Uniform(param_names[i], low=starts[i], high=stops[i])
            params_list.append(param)
        
        return params_list
    
    def read_iteration(self):
        df = pd.read_excel(self.paths.calInput)
        iteration = df.iloc[3,3]
        return iteration
    
    def calibration_log(self):
        calLog = 'calibrateRRI/output/calibration_log'
        return calLog
    
    # ---------- Reading discharge ----------
    def _read_obs_all(self) -> List[pd.Series]:
        obs_list = []
        for fname in self.station_files:
            df = pd.read_csv(self.paths.obs_dir / fname)
            obs_list.append(df.iloc[:, 1])
        return obs_list
    

    # Function to generate parameters
    def parameters(self):
        params = spotpy.parameter.generate(self.params)
        return params
    

    # ---------- Updating RRI input files ----------
    def update_inputs(self, vector):
        with open(self.paths.rri_input, 'r') as file:
            lines = file.readlines()
            
        lines[17] = f"{vector[0]:.3f}     # ns_river (m^(-1/3)s)\n"
        lines[20] = f"{vector[1]:.3f}     # ns_slope (m^(-1/3)s)\n"
        lines[21] = f"{vector[2]:.3f}     # soildepth (m)\n"
        lines[22] = f"{vector[3]:.3f}     # gammaa (-)\n"
        
        lines[24] = f"{vector[4]:.3E}     # kv (m/s)\n"
        lines[25] = f"{vector[5]:.4f}     # Sf (m)\n"
        
        lines[27] = f"{vector[6]:.3E}      # ka (m/s)\n"
        lines[28] = f"{vector[7]:.3f}      # gammam (m)\n"
        lines[29] = f"{vector[8]:.3f}      # beta (-)\n" 
        
        lines[31] = f"{vector[9]:.3E}     # ksg (m/s) -- set zero for no bedrock gw\n"
        lines[32] = f"{vector[10]:.3f}     # gammag (-)\n"
        lines[33] = f"{vector[11]:.3E}     # kg0 (m/s)\n"
        lines[34] = f"{vector[12]:.3f}     # fg (-)\n"
        lines[35] = f"{vector[13]:.3f}     # rgl\n"
        
        lines[38] = f"{vector[14]:.3f}     # width_param_c\n"
        lines[39] = f"{vector[15]:.3f}     # width_param_s\n"
        lines[40] = f"{vector[16]:.3f}     # depth_param_c\n"
        lines[41] = f"{vector[17]:.3f}     # depth_param_s\n"

        with open(self.paths.rri_input, 'w') as file:
            file.writelines(lines)

    def _run_exe(self, exe_path: Path) -> None:
        if not exe_path.exists():
            raise FileNotFoundError(f"Missing executable: {exe_path}")
        subprocess.run([str(exe_path)], check=True)
               
    def read_sim(self):
        sim_path = pd.read_csv(self.paths.sim_dir, header=None).loc[2].item()

        sim_discharge_list = []

        for station_file in self.station_files:
            sim_disc = pd.read_csv(sim_path + station_file[5:-4]+".txt", delimiter=r"\s+", header=None)

            # Extract time and discharge values
            sim_time, sim_discharge = sim_disc[0], sim_disc[1]

            # Generate simulated values for the observed time steps
            sim_discharge_list.append(sim_discharge)

        return sim_discharge_list
    
    def simulation(self, vector):
        self.update_inputs(vector)
        # self._run_exe(self.paths.rri_exe)
        # self._run_exe(self.paths.calcHydro_exe)

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

        for sim_data, obs_data in zip(simulation, evaluation):
            # Calculate RMSE
            rmse = np.sqrt(np.mean((obs_data[:] - sim_data[:]) ** 2))
            rmse_list.append(rmse)

            # Calculate MAE
            mae = np.mean(np.abs(obs_data - sim_data))
            mae_list.append(mae)

            # Calculate R²
            obs_mean = np.mean(obs_data)
            ss_total = np.sum((obs_data - obs_mean) ** 2)
            ss_residual = np.sum((obs_data - sim_data) ** 2)
            r2 = 1 - (ss_residual / ss_total)
            r2_list.append(r2)

        # Average metrics across all stations
        avg_rmse = np.mean(rmse_list)
        avg_mae = np.mean(mae_list)
        avg_r2 = np.mean(r2_list)
        
        # self.plot_hydro(simulation, evaluation, avg_rmse)
        
        # Return a tuple of metrics (you can choose which metrics to include)
        if objFun == "RMSE":
            self.plot_hydro(simulation, evaluation, avg_rmse)
            return avg_rmse
        else:
            self.plot_hydro(simulation, evaluation, avg_mae)
            return avg_mae

        
    # ---------- Plot (optional) ----------
    def plot_hydro(
        self,
        sim_list: Sequence[pd.Series],
        obs_list: Sequence[pd.Series],
        objfunc: float
    ) -> None:
        self.paths.plot_dir.mkdir(exist_ok=True)
        
        # Read input objective function
        df = pd.read_excel(self.paths.calInput)
        objFun = df.iloc[4, 3]
        
        if objFun == "RMSE":
            for fname, sim, obs in zip(self.station_files, sim_list, obs_list):
                sta = Path(fname).stem
                outdir = self.paths.plot_dir / sta
                outdir.mkdir(parents=True, exist_ok=True)

                n = min(len(sim), len(obs))
                simv = sim.iloc[:n].values
                obsv = obs.iloc[:n].values
                t = np.arange(n)

                # Metrics for title
                rmse = np.sqrt(np.mean((obsv - simv) ** 2))
                obs_mean = np.mean(obsv)
                ss_total = np.sum((obsv - obs_mean) ** 2)
                ss_res = np.sum((obsv - simv) ** 2)
                r2 = 1 - ss_res / ss_total if ss_total > 0 else np.nan

                plt.figure(figsize=(8, 3.5))
                plt.plot(t, obsv, color="black", lw=1.2, label="Observation")
                plt.plot(t, simv, color="green", lw=1.2, label="Simulation")
                plt.xlabel("Output step")
                plt.ylabel("Discharge [m³/s]")
                plt.title(f"{sta}\nR²: {r2:.2f}, RMSE: {objfunc:.2f}", fontsize=12)
                plt.legend(ncol=2, fontsize=10)
                plt.grid(axis="y", ls="--")
                plt.tight_layout()

                out = outdir / f"{sta}_rmse_{objfunc}.png"
                plt.savefig(out, dpi=120)
                plt.close()
        else:
            for fname, sim, obs in zip(self.station_files, sim_list, obs_list):
                sta = Path(fname).stem
                outdir = self.paths.plot_dir / sta
                outdir.mkdir(parents=True, exist_ok=True)

                n = min(len(sim), len(obs))
                simv = sim.iloc[:n].values
                obsv = obs.iloc[:n].values
                t = np.arange(n)

                # Metrics for title
                rmse = np.sqrt(np.mean((obsv - simv) ** 2))
                obs_mean = np.mean(obsv)
                ss_total = np.sum((obsv - obs_mean) ** 2)
                ss_res = np.sum((obsv - simv) ** 2)
                r2 = 1 - ss_res / ss_total if ss_total > 0 else np.nan

                plt.figure(figsize=(8, 3.5))
                plt.plot(t, obsv, color="black", lw=1.2, label="Observation")
                plt.plot(t, simv, color="green", lw=1.2, label="Simulation")
                plt.xlabel("Output step")
                plt.ylabel("Discharge [m³/s]")
                plt.title(f"{sta}\nR²: {r2:.2f}, MAE: {objfunc:.2f}", fontsize=12)
                plt.legend(ncol=2, fontsize=10)
                plt.grid(axis="y", ls="--")
                plt.tight_layout()

                out = outdir / f"{sta}_mae_{objfunc}.png"
                plt.savefig(out, dpi=120)
                plt.close()

    