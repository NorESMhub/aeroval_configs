#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Config file for AeroCom PhaseIII optical properties experiment
"""

import os
USER = os.getenv("USER")

DB = {}

OBS_ACCESS = {}
### Define filters for the obs subsets

# BASE FILTERS
ALTITUDE_FILTER = {"altitude": [0, 1000]}

# Setup for models used in analysis
MODELS = {
    "EMAC-DLR": dict(
            model_id="EMAC-DLR-transient2010s",
            model_data_dir="/lustre/storeB/project/aerocom/aerocom1/EMAC-DLR-transient2010s/renamed/"
        ),
    "CESM2-v212": dict(
            model_id="CESM2-v212-transient2010s",
            model_data_dir="/lustre/storeB/project/aerocom/aerocom1/CESM2-v212-transient2010s/renamed/"
        ),
    "EC-Earth3-AerChem": dict(
            model_id="EC-Earth3-AerChem-transient2010s",
            model_data_dir="/lustre/storeB/project/aerocom/aerocom1/EC-Earth3-AerChem-transient2010s/renamed/"
        ),
    "LMDZ-INCA": dict(
            model_id="LMDZ-INCA-transient2010s",
            model_data_dir="/lustre/storeB/project/aerocom/aerocom1/LMDZ-INCA-transient2010s/renamed/"
        ),
    "NorESM2-LM-C": dict(
            model_id="NorESM2-LM-C-transient2010s",
            model_data_dir="/lustre/storeB/project/aerocom/aerocom1/NorESM2-LM-C-transient2010s/renamed/"
        ),
    "OsloCTM3v1-2": dict(
            model_id="OsloCTM3v1-2-transient2010s",
            model_data_dir="/lustre/storeB/project/aerocom/aerocom1/OsloCTM3v1-2-transient2010s/renamed/"
        ),
    "UKESM1-0-LL": dict(
            model_id="UKESM1-0-LL-transient2010s",
            model_data_dir="/lustre/storeB/project/aerocom/aerocom1/UKESM1-0-LL-transient2010s/renamed/"
        ),
}

PLOT_TYPES = {}
for model in MODELS:
    PLOT_TYPES[model] = ["contour", "overlay"]


VAR_OUTLIER_RANGES = {
    "concpm10": [-1, 5000],  # ug m-3
    "concpm25": [-1, 5000],  # ug m-3
    "vmrno2": [-1, 5000],  # ppb
    "vmro3": [-1, 5000],  # ppb
}

EBAS_FILTER = dict(station_name="U*", negate="station_name")
# OBS_GROUNDBASED = {
#     "AeronetSunV3L2": dict(
#         obs_id="AeronetSunV3Lev2.daily",
#         obs_vars=[
#             "od550aer",
#         ],
#         # obs_vars=['od550aer'],
#         # obs_data_dir=AERONET_SUN_LOCAL,
#         obs_vert_type="Column",
#         # obs_vert_type='Surface',
#         obs_filters={**ALTITUDE_FILTER, **AERONET_SITE_FILTER},
#         min_num_obs={"monthly": {"daily": 3}},
#         # web_interface_name='AeronetSunV3L2'),
#     ),
#
#     # "AeronetSDAV3L2": dict(
#     #     obs_id="AeronetSDAV3Lev2.daily",
#     #     # obs_vars=['od550aer', 'ang4487aer'],
#     #     obs_vars=[
#     #         "od550lt1aer",
#     #     ],
#     #     # obs_vars=['od550lt1aer', 'od550gt1aer', ],
#     #     # obs_data_dir=AERONET_SUN_LOCAL,
#     #     obs_vert_type="Column",
#     #     obs_filters={**ALTITUDE_FILTER, **AERONET_SITE_FILTER},
#     #     min_num_obs={"monthly": {"daily": 3}},
#     #     # obs_filters={'od550ltaer': {'ts_type' : 'daily'}},
#     # ),
# }

OBS_GROUNDBASED = {
        ##################
        #    EBAS
        ##################
        "EBAS-m-tc": dict(
            obs_id="EBASMC",
            web_interface_name="EBAS-m",
            obs_vars=[
                # "concNhno3",
                # "concNtno3",
                # "concNtnh",
                # "concNnh3",
                # "concnh4",
                # "prmm",
                # "concpm10",
                # "concpm25",
                # "concSso2",
                # "concNno2",
                # "vmrco",
                # "vmro3max",
                "vmro3",
                # "concNno",
                # "concso4t",
                # "concso4",
            ],
            obs_vert_type="Surface",
            colocate_time=False,
            ts_type="monthly",
            obs_filters=EBAS_FILTER,
        ),
}
# Setup for supported satellite evaluations
OBS_SAT = {}

OBS_CFG = {**OBS_GROUNDBASED, **OBS_SAT}

# DEFAULT_RESAMPLE_CONSTRAINTS = dict(
#     monthly=dict(daily=21),
#     daily=dict(hourly=18)
# )

CFG = dict(
    model_cfg=MODELS,
    obs_cfg=OBS_CFG,
    json_basedir=os.path.abspath(f"/nird/home/{USER}/container.data/aeroval_data/data"),
    coldata_basedir=os.path.abspath(f"/nird/home/{USER}/container.data/aeroval_data/coldata"),
    # var_scale_colmap_file=os.path.abspath(
    #     "/home/jang/data/aeroval-local-web/pyaerocom-config/config_files/c3s2/var_scale_colmap.ini"),
    # io_aux_file=os.path.abspath(
    #     "/home/jang/data/aeroval-local-web/pyaerocom_config/eval_py/gridded_io_aux.py"
    # ),
    # if True, existing colocated data files will be deleted
    reanalyse_existing=True,
    only_json=False,
    add_model_maps=True,
    only_model_maps=False,
    # maps_freq="yearly",
    plot_types=PLOT_TYPES,
    # boundaries={
    #         "west": -180,
    #         "east": 180,
    #         "north": 90,
    #         "south": -90,
    #     },
    # clear_existing_json=False,
    clear_existing_json=True,
    # if True, the analysis will stop whenever an error occurs (else, errors that
    # occurred will be written into the logfiles)
    raise_exceptions=False,
    # Regional filter for analysis
    filter_name="ALL-wMOUNTAINS",
    # colocation frequency (no statistics in higher resolution can be computed)
    ts_type="daily",
    map_zoom="World",
    freqs=["monthly", "yearly"],
    # periods=['2020-2021', '2021'],
    periods=["2010-2019", ],
    main_freq="monthly",
    # stats_main_freq = 'daily',
    zeros_to_nan=False,
    # add_trends=True,
    # trends_min_yrs=3,
    # min_num_obs=DEFAULT_RESAMPLE_CONSTRAINTS,
    # colocate_time=True,
    obs_remove_outliers=False,
    model_remove_outliers=False,
    harmonise_units=True,
    # regions_how='htap',
    regions_how="default",
    annual_stats_constrained=False,
    proj_id="HYwaySurface",
    exp_id="transient2010s",
    exp_name="transient2010s",
    exp_descr=("Ground based evaluation of simulation one data of the HYway project."),
    exp_pi="Jan Griesfeller (jan.griesfeller@met.no)",
    public=True,
    obs_cache_only=True,
    # directory where colocated data files are supposed to be stored
    weighted_stats=True,
    # start='2020-12-01',
    # stop ='2021-02-28',
    var_order_menu=[
        "vmro3",
        "concso4",
        "od550dust",
        "ang4487aer",
        "vmrno2",
    ],
)

if __name__ == "__main__":
    from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
    import json
    stp = EvalSetup(**CFG)

    # stp = EvalSetup(proj_id='BLA', exp_id='blub',obs_cfg=OBS)

    ana = ExperimentProcessor(stp)
    print(stp)
    # file = "./c3s3_fast_and_simple_cfg.json"
    # with open(file, "w") as fh:
    #     json.dump(CFG, fh, indent=4)

    # ana.exp_output.delete_experiment_data()
    # res=ana.exp_output._results_summary()
    # ana.update_interface()
    # ana.exp_output.delete_experiment_data()

    # data = ana.read_model_data('AEROCOM-MEDIAN', 'od550gt1aer')
    res = ana.run()
