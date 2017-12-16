openfoem-run-time-viewer
====

It is OpenFOAM of computation time prediction.
## Description

`openfoem-run-time-viewer` is GUI tool that show computation time prediction.


## Requirement

* pip
* python3
* OpenFOAM(etc/bashrc has been readed)
## QuickStart(Example)

```
git clone https://github.com/kurenaif/openfoam-run-time-viewer
cd openfoam-run-time-viewer
pip install -r requirements.txt
cd $WM_PROJECT_DIR/tutorials/compressible/rhoCentralFoam/wedge15Ma5
blockMesh
foamJob rhoCentralFoam
cd -
python app.py $WM_PROJECT_DIR/tutorials/compressible/rhoCentralFoam/wedge15Ma5/log 0.2
# (access localhost:8000 with browser)
```

## Usage

### 1. Calc someone with `foamJob`
```
foamJob XXXXXX
```

or you can manuary

```
XXXXXX > log
```

### 2. move to This repository and run

```
cd path/to/openfoam-run-time-viewer
python app.py path/to/OpenFOAM/caseDir/log end_time
```

## about app.py

```
usage: app.py [-h] file_path end_time

Predict calculation end time

positional arguments:
  file_path   log file path
  end_time    calculation end time

optional arguments:
  -h, --help  show this help message and exit
```

## Installation

```
git clone https://github.com/kurenaif/openfoam-run-time-viewer
cd openfoam-run-time-viewer
pip install -r requirements.txt
```

## Author

[@fwarashi](https://twitter.com/fwarashi)