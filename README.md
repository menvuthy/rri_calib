# Auto‑Calibration Program for Rainfall-Runoff Inundation (RRI) Model in Python

---

*<font color='grey'>**Developer:** Men Vuthy (MEng), Water Resources and Energy Department, Nippon Koei, 2026*</font> 

---

This repository provides a **Python‑based automatic calibration framework** for the  
**Rainfall–Runoff–Inundation (RRI) model** using the **SCE‑UA** global optimization algorithm implemented via **SPOTPY**.

The framework is designed to automate RRI model calibration, reduce manual trial‑and‑error, and improve reproducibility in hydrological and flood modeling studies.

---

## Key Features

- Automatic calibration of RRI model parameters
- Global optimization using the SCE‑UA algorithm
- Integration with SPOTPY optimization framework
- Support for common objective functions (RMSE, MAE, R²)
- Flexible parameter range definition
- CSV‑based logging of calibration results
- Reproducible environment using Conda (`environment.yml`)

---

## Calibration Workflow

The auto‑calibration process follows these steps:

1. Initialize the RRI calibration model
2. Read calibration settings and parameter ranges
3. Load observed discharge data
4. Execute repeated RRI simulations
5. Evaluate model performance using an objective function
6. Search for optimal parameters using SCE‑UA
7. Save calibration logs and optimal parameter sets

---

## Repository Structure (Example)

project_root/
│
├─ rri_calib/
│   ├─ init.py
│   └─ calibrator.py        # CalibrateRRI class
│
├─ notebooks/
│   └─ run_calibration.ipynb
│
├─ data/
│   ├─ obs/                 # Observed discharge (CSV)
│   └─ sim/                 # RRI simulation outputs
│
├─ environment.yml          # Conda environment (recommended)
├─ ParameterSetting.xlsx    # Calibration parameter definition
└─ README.md

## Requirements

This notebook requires a Conda environment with the following main dependencies:

- Python (recommended: 3.10)
- SPOTPY
- NumPy
- Pandas
- SciPy
- Matplotlib

The environment can be created using the provided `environment.yml` file.


## Input Data

The following inputs are required before running the calibration:

- Observed discharge data (CSV format)
- RRI model input files and executable
- Parameter ranges defined in `ParameterSetting.xlsx`
- Number of calibration iterations
- Selected objective function (e.g. RMSE or MAE)

Please ensure that all input files are correctly configured before execution.


## Running the Auto‑Calibration

The code cell below initializes the calibration model, sets up the SCE‑UA sampler,
and starts the optimization process.

Depending on the number of iterations and model complexity, the calibration may
require significant computation time.


## Outputs

The calibration produces the following outputs:

- CSV log file containing objective function values and parameter sets
- Optimal parameter combination identified by SCE‑UA
- (Optional) Hydrograph plots comparing observed and simulated discharge

These results can be used for validation, sensitivity analysis, or further simulations.

## Notes

- Calibration results depend strongly on the quality of observed data and the
  selected parameter ranges.
- It is recommended to verify calibrated parameters against physical
  and hydrological plausibility.
- Long calibration runs are advised to ensure stable convergence of the SCE‑UA algorithm.