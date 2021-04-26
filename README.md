# Circuit Evaluator


Evaluate boolean circuits stored in [Bristol Fashion](https://homes.esat.kuleuven.be/~nsmart/MPC/).

The evaluator supports two inputs and an arbitrary number of outputs. 

## Getting Started

``python evaluator.py`` runs adder64 with two random inputs.

### Optional arguments

``-f`` set the filepath for the circuit you want to execute (default: ./adder64.txt)

``-a`` set the first input of the circuit (default: Random input)

``-b`` set the second input of the circuit (default: Random input)

``-c`` specify the format of your circuit you want to execute (default: bristol_fashion)

``-fu`` specify which functionality your circuit executes. If the circuit executes add64, sub64, or mult64 the circuit output can be compared to the expected result of the functionality.

### Example 
```
python evaluator.py -f ./sub64.txt -a 5555 -b 222 -fu sub64
```

Evaluates circuit file **sub64.txt** with inputs **5555** and **222**. Functionality was set to sub64. Thus the result is compared to an expected result **(a-b)**.

The function call outputs:

```
Circuit loaded into memory in 0.0005847999999999964 seconds
Finished evaluating circuit in 0.0007237999999999967 seconds
ina 5555
inb 222
circuit output 0:  5333
expected_result 5333
circuit output and expected result match
```