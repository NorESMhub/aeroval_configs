# Container setup on the sigma2 infrastructure
This file contains documentation about running pyaerocom in a container on sigma2 infrastructure.

For the moment `nird` ans `betzy` are covered. The reason for seperate coverage is that nird doesn't support 
the Linux user-space mounting infrastructure `fuse` that apptainer is depending on. In addition, 
containers are not officially supported by sigma2 on `nird`.

## Prerequests
Note that `singularity` is the former name of `apptainer`. Besides some newer development, the both commands can be used interchangeably.

- a working apptainer / singularity installation 
- internet access
- - access to dockerhub

## creating the pyaerocom container
The apptainer definition file pyaerocom.def is supplied [here](./apptainer/pyaerocom.def) and is listed below:
```
BootStrap: docker
From: python:3.12

%post
   apt -y update
   apt -y upgrade
   pip install --no-cache-dir pyaerocom
   pip install --no-cache-dir pyaro-readers
   python -m pip install --no-cache-dir 'git+https://github.com/metno/pyaerocom-parallelization.git'

%environment
   export LC_ALL=C

%labels
    Author JanG
```

The pyaerocom container can be built with the command
```bash
apptainer build <path to sif file> pyaerocom.def
```

## Running on nird
Although there is apptainer installed on the `nird3` login node at the time of this writing, it's not working due to the 
missing `fuse` support on the nird login nodes. `singularity` on the other hand doesn't need `fuse` and is still able to 
run the pyaerocom container. Also those created using `apptainer`.

To get a working version of `singularity`, one can either compile one or just install `singularity` using `mamba` and 
the `conda-forge` channel. command `mamba create -n singularity singularity` will install `singularity` in a new environment
named `singularity` assuming that you have a working mamba in your environment.

This documentation assumes that you have installed `singularity` as above.

You can test if your singularity install worked as expected with the command
```
mamba run -n singularity singularity --version
```

The output should look like this:
```
singularity version 3.8.6
```

To make the documentation a bit simpler, we assume that the user is using the following directory structure to run the container:
### directory structure

| path | container location for the examples | purpose |
|---------------------------|---------|-------------------|
|${BaseDir}/MyPyaerocom     | /nird/home/${USER}/MyPyaerocom | ~/MyPyaerocom directory (standard user specific pyaerocom directory) |
|${BaseDir}/pyaerocom_data  | /lustre/storeB/project/aerocom/aerocom1 | directory with model / observational data | 
|${BaseDir}/aeroval_data    | /nird/home/${USER}/container.data/aeroval_data | output directory of aeroval | 
|${BaseDir}/aeroval_configs | /nird/home/${USER}/container.data/aeroval_configs |directory containing the aeroval config file | 
|${BaseDir}/aeroval_logs    | /nird/home/${USER}/container.data/aeroval_logs| directory containing the pyaerocom log file | 

Please note that directory structure `/nird/home/${USER}/container.data/` has to exist since the container inherits the user's home directory.
They can be created using the following command:

```bash
mkdir -p ~/container.data/aeroval_data ~/container.data/aeroval_configs ~/container.data/aeroval_logs
```

### first testing
#### check which cache files are available in the container
TODO: make example less specific

```shell
apptainer exec --bind /lustre/storeB:/lustre/storeB --bind ~/MyPyaerocom.apptainer:/home/${USER}/MyPyaerocom ~/tmp/apptainer/pyaerocom.sif pya listcache
```

#### create cachefiles using the container
This will work 

```shell
apptainer exec --bind /lustre/storeB:/lustre/storeB --bind ~/MyPyaerocom.apptainer:/home/${USER}/MyPyaerocom ~/tmp/apptainer/pyaerocom.sif pyaerocom_cachegen --vars vmro3 -o EBASMC
```

#### Example (for the HYway project)

To run the standard 2d analysis:

```shell
singularity exec \
--bind /nird/datapeak/NS11106K/HYway/modelling_repository/pyaerocom/MyPyaerocom.apptainer:/nird/home/${USER}/MyPyaerocom \
--bind /nird/datapeak/NS11106K/HYway/modelling_repository/pyaerocom/pyaerocom_data:/lustre/storeB/project/aerocom/aerocom1 \
--bind /nird/datapeak/NS11106K/HYway/modelling_repository/pyaerocom/aeroval_data:/nird/home/${USER}/container.data/aeroval_data \
--bind /nird/datapeak/NS11106K/HYway/modelling_repository/pyaerocom/aeroval_configs:/nird/home/${USER}/container.data/aeroval_configs \
--bind /nird/datapeak/NS11106K/HYway/modelling_repository/pyaerocom/aeroval_logs:/nird/home/${USER}/container.data/aeroval_logs \
--env "PYAEROCOM_LOG_FILE=/nird/home/${USER}/container.data/aeroval_logs/aerocom.log" \
/nird/datapeak/NS11106K/HYway/modelling_repository/pyaerocom/bin/pyaerocom.sif \
python /nird/home/${USER}/container.data/aeroval_configs/projects/HYway/cfg_HYway_2d.py
```

Note that the data will appear on the original file locations 
(below `/nird/datapeak/NS11106K/HYway/modelling_repository/pyaerocom/`). The directory structure `~/container.data` is only 
used within the container, but helps to create easily reusable aeroval config files.

