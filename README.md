# GGG Pulse field processing code

Data processing code written specifically for processing magnetic field pulses. The module 
[pulse_processing.py](https://github.com/dgglab/pulsed_field/blob/master/modules/pulse_processing.py) contains code for importing and processing the generated data. Specifically, the rising/falling portions of a magnetic field pulse are extracted and multiple magnetic field pulses can be interpolated to the same magnetic fields for further processing. 

## Installing
The code requires the NI module for working with TDMS files (ASCII files can be processed as well, but are much slower).
```
pip install nptdms
```

## Examples
See [example.ipynb](https://github.com/dgglab/pulsed_field/blob/master/example.ipynb) for a demo.
