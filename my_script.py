#using this data before other raw data is too large
#this is more focused on branch prediction testing 

#main point for simulator: 
#   -read a branch trace (a sequence of instructions with branch info)
#   -pass the branch inst. to my branch predictor
#   -collect stats on how well my predictor performs 
#   -provide metrics (misprediction rate, MR per kilo inst., Inst per cycle, wrong-path cycle)
#   -can compare predictors without needing to run a full CPU simulation 


#how it works
#set up the predictor state
#each inst. in trace - notify inst fetch/ for conditional branch: cond dir prediction
#update predictor with actual outcome spec update
#other pipeline notifications
#end predictor 
#print metrics 

#check to see that all files are reading 

import os
import subprocess 
import csv
import pandas as pd 


#when reading in the second results data, create a definition to make it easier
#reading text file to cvs 

def parse_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Step 2: initialize attributes
    traces = []
    metrics = {}
    #find traces
    for line in lines:
        line = line.strip()
        if line.startswith("running trace:"):
            trace_name = line.split(":")[1].strip()
            traces.append({"trace": trace_name})

            metrics[trace_name] = {"instructions": None, "cycles": None, "IPC": None, 
                                   "NumBr": None, "MispBr": None, "MR": None, "MPKI": None}

    #extract the needed data 
    current_trace = None
    for line in lines:
        line = line.strip()

        if line.startswith("running trace:"):
            current_trace = line.split(":")[1].strip()

        if current_trace:
            if line.startswith("instructions ="):
                metrics[current_trace]["instructions"] = int(line.split('=')[1].strip())
            elif line.startswith("cycles       ="):
                metrics[current_trace]["cycles"] = int(line.split('=')[1].strip())
            elif line.startswith("IPC          ="):
                metrics[current_trace]["IPC"] = float(line.split('=')[1].strip())



    current_trace = None
    capture_next_line = False

    for line in lines:
        line = line.strip()

        #find the beginning of the trace 
        if line.startswith("running trace:"):
            current_trace = line.split(":")[1].strip()

        #find the header of table 
        if line.startswith("Type") and "NumBr" in line:
            capture_next_line = True
            continue

        if capture_next_line and current_trace:
            if line.startswith("CondDirect"):
                parts = line.split()
                
                metrics[current_trace]["NumBr"] = int(parts[1])
                metrics[current_trace]["MispBr"] = int(parts[2])
                metrics[current_trace]["MR"] = float(parts[3].replace('%', ''))
                metrics[current_trace]["MPKI"] = float(parts[4])

                capture_next_line = False
    
    return traces, metrics


#read in my result files 
bimodal_file_path = r"C:/Users/dino1/cbp2025/all_int_results_bimodal.txt"
tage_file_path = r"C:/Users/dino1/cbp2025/all_int_results_tage.txt"

#call the function 
bimodal_traces, bimodal_metrics = parse_file(bimodal_file_path)
tage_traces, tage_metrics = parse_file(tage_file_path)


#cretae a function to build the dataframe i will use to compare data 
def build_df(traces, metrics, predictor_name):
    df = pd.DataFrame(traces)

    df["Predictor"] = predictor_name
    df["instructions"] = df["trace"].apply(lambda x: metrics[x]["instructions"])
    df["cycles"] = df["trace"].apply(lambda x: metrics[x]["cycles"])
    df["IPC"] = df["trace"].apply(lambda x: metrics[x]["IPC"])
    df["NumBr"] = df["trace"].apply(lambda x: metrics[x]["NumBr"])
    df["MispBr"] = df["trace"].apply(lambda x: metrics[x]["MispBr"])
    df["MR"] = df["trace"].apply(lambda x: metrics[x]["MR"])
    df["MPKI"] = df["trace"].apply(lambda x: metrics[x]["MPKI"])

    #print(metrics["int_0_trace"])

    #compute cycles per instruction CPI
    df["CPI"] = df["cycles"] / df["instructions"]

    return df 

#call the dataframe function for bimodal and tage 
bimodal_df = build_df(bimodal_traces, bimodal_metrics, "Bimodal")
tage_df = build_df(tage_traces, tage_metrics, "Tage")

final_df = pd.concat([bimodal_df, tage_df], ignore_index = True)

print(final_df.head(14))









