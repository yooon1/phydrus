"""
Example script of how to setup a basic HYDRUS-1D model using Pydrus.

Author: R.A. Collenteur, University of Graz, 2019

"""

import os

import pandas as pd

import phydrus as ps

ws = "example2"
exe = os.path.join(os.getcwd(), "hydrus")

# Create the basic model
desc = "Example 2 - Grass Field Problem (Hupselse Beek 1982)"

ml = ps.Model(exe_name=exe, ws_name=ws, name="model", description=desc,
              mass_units="-", time_unit="days", length_unit="cm")

times = ml.add_time_info(tinit=90, tmax=273, print_times=True)

# Water inflow parameters
ml.add_waterflow(linitw=False, top_bc=3, bot_bc=4, ha=1e-6, hb=1e4)

m = ml.get_empty_material_df(n=2)

m.loc[[1, 2]] = [[0.0001, 0.399, 0.0174, 1.3757, 29.75, 0.5],
                 [0.01, 0.339, 0.0139, 1.6024, 405.34, 0.5]]

ml.add_material(m)

profile = ps.create_profile(0, [-100, -230], h=-200, dx=10, mat=m.index)
ml.add_profile(profile)
ml.add_obs_nodes([10, 20])

atm = pd.read_csv("data/ex2.csv", index_col=0)
ml.add_atmospheric_bc(atm)

ml.add_root_uptake(model=0, poptm=[-25, -25])
ml.add_root_growth(2, irfak=1, trmin=0, trmed=0, trmax=2143, xrmin=10,
                   xrmed=0, xrmax=50, trperiod=365)
ml.write_input()
rs = ml.simulate()

df = ml.read_tlevel()
df.plot(subplots=True)
