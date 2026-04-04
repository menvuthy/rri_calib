import spotpy
from rri_calib import CalibrateRRI

# --------------------------------------------------
# Initialize RRI calibration model
# --------------------------------------------------
RRI_model = CalibrateRRI()

# --------------------------------------------------
# Load calibration parameters and settings
# --------------------------------------------------
iteration = RRI_model.read_iteration()
log_sheet = RRI_model.calibration_log()

# --------------------------------------------------
# Apply SCE-UA optimization algorithm
# --------------------------------------------------
sampler = spotpy.algorithms.sceua(
    RRI_model,
    dbname=log_sheet,
    dbformat="csv"
)

# --------------------------------------------------
# Start auto-calibration
# --------------------------------------------------
sampler.sample(iteration)