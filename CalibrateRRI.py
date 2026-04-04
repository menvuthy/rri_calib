import spotpy
from rri_calib import CalibrateRRI

# Load Class
RRImodel = CalibrateRRI()
iteration = RRImodel.read_iteration()
log_sheet = RRImodel.calibration_log()

# Apply SCE-UA algorithm
sampler = spotpy.algorithms.sceua(RRImodel, dbname=log_sheet, dbformat='csv')

# Start Calibration
sampler.sample(iteration)