### Load Value Prediction

The purpose of load value prediction is to be able to predict the value of a memory load instruction.

Recall that memory accesses can be hundreds or thousands of cycles and can lead to significant pipeline stalls, especially on cache misses.
One unique solution around this is to be able to predict the value of the load instruction and speculatively execute based on the predicted load value.
Later when the actual memory load value returns, we can compare and check to see if our load value was correctly predicted or not.
Similar to our branch misprediction scenario in speculative tomasulo, if our load value is mispredicted we simply rollback by flushing the ROB.
If we correctly predicted, then great! We continue running on and benefited from executing instructions speculatively.

A major reason why value prediction works is that programs tend to exhibit value similarity behaviors where values tend to be similar either spatially (neighboring memory addresses) or temporally (repeated access to the same memory location does not change, for example, a constant value in memory).

## Install
This project entails usage of below 3 packages which can be easily installed:
numpy - for computation 
pandas - to generate results of all configuration and export it
XlsxWriter - to export the 2D-array to excel
```
$ pip install numpy
$ pip install pandas
$ pip install XlsxWriter
```

 
## Usage

### CLI
#### Simple predictor
Default configuration is: This implements only LVPT and LCT, the default configuration of 10 bit for LCPT and 8 bit for LCT is taken. It only requires the name of the trace file.

```
$ python simple_predictor.py ./traces/pintrace5.out
```

#### Prediction Outcome History
For this predictor, we run 60 different kind of configuration listed in config file. We keep no. of bits in saturating counter constant at all times. Any change to other configuration can be done here.  <br />
The tracefile to run for can also be updated in config.

#### Config 
We use config file, to pass parameters to the module. Any change to parameters should be done in config file. 

LVPT_index : this parameter choses the n of LSB from PC address. It determines how big the tablw would be <br />
LVPT_hist_bit: it stores the history depth i.e the no. of past history of the predictions  <br />
Counter_bit: 4 (kept as constant) <br />
threshold: this parameter can be tweaked based on what threshold we want to predict  <br />
penalty: the penalty by which we want to decrease our confidence if we predict wrong <br />

#### Run
It has two modules. PredOutcomeHistory.py is the main module and PredTable_wrapper.py is the wrapper that calls PredOutcomeHistory for different configurations given in config.

```
$ python PredTable_wrapper.py
```

Note: Running more configuration could be very time consuming. It took around 20-25 minutes to run 312 kind of configurations. 
We would recommend to stick to lower number of configurations for quicker results.
