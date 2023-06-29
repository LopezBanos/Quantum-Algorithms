#######################################################################################
#                                IMPORTING PACKAGES                                   #
#######################################################################################
import os
import time
import dimod           # D-WAVE share API for samplers [1]
import neal
import tabu
import numpy as np     # Python Scientific Package     [2]
import pandas as pd    # Pandas (Data management)      [3]
from utils import path_for_any_os, QAP_problem
from dimod import ConstrainedQuadraticModel,BinaryQuadraticModel, Binary, quicksum

#######################################################################################
#                                LOADING DATA                                         #
#######################################################################################
# Files to read
CURRENT_DIRECTORY = os.getcwd()
PARENT_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
FILE_PATH = os.path.join(PARENT_DIRECTORY, 'instances', 'QAP')
FILES_TO_READ = os.listdir(FILE_PATH) # (list) Name of txt files

# Open the file
file = open("QAP_csv/QAP_RunTime.txt", "w")

# Loop to read files and solve the instances:
for file_name in FILES_TO_READ:
    # Start timing
    start = time.time()

    # Path to file
    path = path_for_any_os('QAP', file_name)

    # Name of the file
    NAME = file_name.replace('.txt', '')

    # Problem size
    S = int(pd.read_csv(path, delim_whitespace=True, nrows=1, header=None).iloc[0].to_list()[0])

    # TIMEOUT: Total time of annealing execution for tabu solver
    ONE_MIN = 60000
    TIMEOUT = ONE_MIN + (S//10)*ONE_MIN # Add an extra minute of execution time every 10 more variables

    if 'dre' in NAME: #USING BQM to FORMULATE THE PROBLEM + tabu solver to Fix execution time    
        skip = 1
        print('Solving Instance ', NAME)

    #######################################################################################
    #                                BUILDING BQM                                         #
    #######################################################################################
        bqm = QAP_problem(path, skip)

    #######################################################################################
    #                                 TABU SOLVER                                         #
    #######################################################################################
        sampler = tabu.TabuSampler()
        results = sampler.sample(bqm, timeout=TIMEOUT) # Output the best solution found in the given time
        index_columns = ['energy', 'num_occurrences']
        for i in range(S):
            for j in range(S):
                index_columns.append('x_{}_{}'.format(i+1,j+1))
        results_table = results.to_pandas_dataframe()[index_columns].sort_values(by=['energy'])
        pd.set_option('display.max_rows', 7)
        pd.set_option('display.max_columns', 500)
        results_table.to_csv('QAP_csv/{}.csv'.format(NAME))

        end = time.time()

        # Write RunTime in file
        file.write(NAME)
        file.write(' RunTime: ')
        file.write('{}'.format(end - start))
        file.write('(s)\n')
        print('RunTime: ', end - start)
#=====================================================================================#
#=====================================================================================#
    else:
        # USING CQM to FORMULATE THE PROBLEM + SimulatedAnnealingSampler
        skip = 2
        print('Solving Instance ', NAME)

        # Path to file
        path = path_for_any_os('QAP', file_name)
    #######################################################################################
    #                                BUILDING BQM                                         #
    #######################################################################################
        bqm = QAP_problem(path, skip)

    #######################################################################################
    #                             SIMULATED ANNELING                                      #
    #######################################################################################
        results = neal.sampler.SimulatedAnnealingSampler().sample(bqm, num_reads=100, 
                                                                num_sweeps=100*S, 
                                                                num_sweeps_per_beta=S)
        results_table = results.to_pandas_dataframe()
        index_columns = ['energy', 'num_occurrences']
        for i in range(S):
            for j in range(S):
                index_columns.append('x_{}_{}'.format(i+1,j+1))
        results_table = results_table[index_columns].sort_values(by=['energy'])
        pd.set_option('display.max_rows', 7)
        pd.set_option('display.max_columns', 500)
        results_table.to_csv('QAP_csv/{}.csv'.format(NAME))

        end = time.time()

        # RunTime
        file.write(NAME)
        file.write(' RunTime: ')
        file.write('{}'.format(end - start))
        file.write('(s)\n')
        print('RunTime: ', end - start)

#print('The total RunTime has been ', end, '(s)')
file.close()