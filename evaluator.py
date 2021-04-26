import os
import sys
import random
from operator import xor
import helperfunctions as hf
import time
import argparse


def executeCircuit(filepath, circuit_format='bristol_fashion', input_a='r', input_b='r', function=''):
    if circuit_format != 'bristol_fashion':
        print('Supported circuit formats: bristol_fashion')
        raise
    
    circuit = []
    functions = ['sub64', 'adder64', 'mult64']

    #read bristol circuit file

    circuit_reading_beginning = time.perf_counter()

    with open(filepath, "r") as f:
        index = 0
        for line in f:
            gate_elements = line.rstrip("\n").split(" ")
            if len(gate_elements) > 1:
                circuit.append(gate_elements)

    num_wires = int(circuit[0][1])
    num_gates = int(circuit[0][0])

    if circuit_format == 'bristol_fashion':
        bitlength_input_a = int(circuit[1][1])
        bitlength_input_b = int(circuit[1][2])
        bitlength_outputs = int(circuit[2][1])
        num_outputs = int(circuit[2][0])
        #bitlength_outputs = 64
        #num_outputs = 1
        #bitlength_outputs = 128

    
    circuit_reading_finished = time.perf_counter()

    print("Circuit loaded into memory in {} seconds".format(circuit_reading_finished-circuit_reading_beginning))

    elements = {}

    #print(num_gates, num_wires, bitlength_input_a, bitlength_input_b, bitlength_outputs)

    # convert/generate inputs for a and b

    circuit_evaluation_beginning = time.perf_counter()

    if input_a == 'r':
        for i in range(bitlength_input_a):
            elements[bitlength_input_a-1-i] = bool(random.getrandbits(1))
    else:
        input_a = int(input_a)        
        bit_representation = hf.convert_int_to_boolarr(input_a,bitlength_input_a)
        print(bit_representation, len(bit_representation))
        for i in range(len(bit_representation)):
            elements[i] = int(bit_representation[-1-i])
        


    if input_b == 'r':
        for i in range(bitlength_input_b):
            elements[bitlength_input_a+bitlength_input_b-1-i] = bool(random.getrandbits(1))
    else:
        input_b = int(input_b)  
        bit_representation = hf.convert_int_to_boolarr(input_b,bitlength_input_b)
        print(bit_representation)
        for i in range(len(bit_representation)):
            elements[i+bitlength_input_a] = int(bit_representation[-1-i])

    #execute circuit, XOR, AND, NOT supported

    for i in range(len(circuit[3:])):
        if circuit[i+3][4] == 'INV':
            output_wire = not elements[int(circuit[i+3][2])]
            elements[int(circuit[i+3][3])] = output_wire
        else:
            if circuit[i+3][5] == 'XOR':
                output_wire = xor(elements[int(circuit[i+3][2])], elements[int(circuit[i+3][3])])
                elements[int(circuit[i+3][4])] = output_wire        
            else:
                output_wire = elements[int(circuit[i+3][2])] and elements[int(circuit[i+3][3])]
                elements[int(circuit[i+3][4])] = output_wire   
            

    circuit_evaluation_finished = time.perf_counter()

    print("Finished evaluating circuit in {} seconds".format(circuit_evaluation_finished-circuit_evaluation_beginning))



    input_a = 0
    for i in range(bitlength_input_a):
        input_a = (input_a << 1) | elements[bitlength_input_a-1-i]

    print("ina",input_a)

    input_b = 0
    for i in range(bitlength_input_b):
        input_b = (input_b << 1) | elements[bitlength_input_a+bitlength_input_b-1-i]

    print("inb",input_b)


    output = []
    
    for i in range(num_outputs):
        output.append([])
        for j in range(bitlength_outputs):
            to_add = elements[num_wires-1-j-(bitlength_outputs*i)]    
            output[i].append(to_add)


        #print("output",output)
    out = []
    for i in range(num_outputs):
            #out.append([])
            out.append(0)
            for bit in output[i]:
                out[i] = (out[i] << 1) | bit

            print("circuit output {}: ".format(i),out[i])
    


    if function in functions:
        expected_result = -1
        if function == 'adder64':
            expected_result = input_a+input_b       

        elif function == 'mult64':
            expected_result = input_a*input_b
        elif function == 'sub64':
            expected_result = input_a-input_b

        
        print("expected_result", expected_result)

        if expected_result == out[0]:
            print('circuit output and expected result match')
        else:
            print('circuit output and expected result do not match')
        
        if(expected_result >= 2**bitlength_outputs):
            print("output overflows bitlength ({}-bit)! Thus, results do not match.".format(bitlength_outputs))

   

        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--circuitformat", type=str, default= "bristol_fashion")
    parser.add_argument("-a", "--input_a", type=str, default='r')
    parser.add_argument("-b", "--input_b", type=str, default='r')
    parser.add_argument("-f", "--filepath", type=str, help="path of the circuit file to execute",default="./adder64.txt")
    parser.add_argument("-fu", "--function", type=str, default='')


    args = parser.parse_args()

    filepath = args.filepath
    circuit_format = args.circuitformat
    input_a = args.input_a
    input_b = args.input_b
    function = args.function
    #input_a = int('1561561555555')
    #input_b = int('4894894')
    
    #function = ''
    #filepath = './aes_256.txt'
    #executeCircuit(filepath, input_a=input_a, input_b=input_b, function='mult64')
    
    
    executeCircuit(filepath, circuit_format, input_a, input_b, function)

if __name__ == "__main__":
    main()