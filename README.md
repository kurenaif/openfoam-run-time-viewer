openfoem-run-time-viewer
====

It is OpenFOAM of computation time prediction.
## Description

`openfoem-run-time-viewer` is GUI tool that show computation time prediction.

### GUI output
![](doc/sample.gif)

### CUI output
```
{'Time': 0.0992, 'ExecutionTime': 89.49}
excepted end time:  2017-12-17 01:16:44.052353
reaming time:  95.56235294117648 sec.
{'Time': 0.0993, 'ExecutionTime': 89.58}
excepted end time:  2017-12-17 01:16:44.047549
reaming time:  95.46754901960786 sec.
{'Time': 0.0994, 'ExecutionTime': 89.66}
excepted end time:  2017-12-17 01:16:44.032745
reaming time:  95.37274509803925 sec.
```

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
# kill task (Ctrl+c on terminal)
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

### 3. kill GUI
kill GUI but don't stop calculation 

```
Ctrl+C (on terminal)
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