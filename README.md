# Auto‑Calibration Program for Rainfall-Runoff Inundation (RRI) (Python)

This repository provides a **Python‑based automatic calibration framework** for the  
**Rainfall–Runoff–Inundation (RRI) model** using the  
**Shuffled Complex Evolution – University of Arizona (SCE‑UA)** global optimization algorithm
implemented via **SPOTPY**.

The framework is designed to automate RRI model calibration, reduce manual trial‑and‑error,
and improve reproducibility in hydrological and flood modeling studies.

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

``