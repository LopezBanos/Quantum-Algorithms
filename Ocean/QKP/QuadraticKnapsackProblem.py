#######################################################################################
#                                IMPORTING PACKAGES                                   #
#######################################################################################
import os
import time
import dimod           # D-WAVE share API for samplers [1]
import numpy as np     # Python Scientific Package     [2]
import pandas as pd    # Pandas (Data management)      [3]
from utils import path_for_any_os
from dimod import ConstrainedQuadraticModel,BinaryQuadraticModel, Binary, quicksum

#######################################################################################
#                                LOADING DATA                                         #
#######################################################################################
# Files to read
CURRENT_DIRECTORY = os.getcwd()
PARENT_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
FILE_PATH = os.path.join(PARENT_DIRECTORY, 'instances', 'QKP')
FILES_TO_READ = os.listdir(FILE_PATH) # (list) Name of txt files

file = open("QKP_csv/QKP_RunTime.txt", "w")
# Loop to read files and solve the instances:
for file_name in FILES_TO_READ:

    start = time.time()
    # Path to file
    path = path_for_any_os('QKP', file_name)

    # Name of the file
    NAME = pd.read_csv(path, skiprows=0, delim_whitespace=True, nrows=1, header=None).iloc[0].to_list()[0]
    print('Solving Instance ', NAME)
    # Number of decision variables
    N = int(pd.read_csv(path, skiprows=1, delim_whitespace=True, nrows=1, header=None).iloc[0].to_list()[0])

    # Objective function coefficients (No constraints)
    df_obj = pd.read_csv(path, skiprows=2, delim_whitespace=True, nrows=N, header=None)

    # Sanity check
    print('The total number of decision variables is ', N)


#######################################################################################
#                                KNAPSACK COEFFICIENTS                                #
#######################################################################################
    # Diagonal terms (i=j)
    v = df_obj.iloc[0].to_list()

    # Crossed terms (i != j)
    vv = []
    for i in range(1,N):
        line_list = df_obj.iloc[i].to_list()
        # Clean nan values
        cleanedList = [x for x in line_list if str(x) != 'nan']
        vv.append(cleanedList)

    # Convert the list of list into a np.array (either you can have a list of list and iterate over it
    # where the first list correspond to all the combinations of the first variable x1x2 x1x3 x1x4 ...)
    vv = [item for sublist in vv for item in sublist]


#######################################################################################
#                                    CONSTRAINTS                                      #
#######################################################################################
    # Constraints coefficients
    df_constraints = pd.read_csv(path, delim_whitespace=True, skiprows=N+5, nrows=1, header=None)
    a = df_constraints.iloc[0].to_list()

    # Constraint upper bound
    df_upper_bound = pd.read_csv(path, delim_whitespace=True, skiprows=N+4, nrows=1, header=None)
    b = df_upper_bound.iloc[0].to_list()[0]

#######################################################################################
#                                    BUILD THE CQM                                    #
#######################################################################################
    cqm = ConstrainedQuadraticModel()
    # Create the variables classes(CQM admits integer variables)
    bin_variables = [Binary('x_{}'.format(i+1)) for i in range(N)]
    index_columns = ['energy', 'num_occurrences']
    for i in range(N):
        index_columns.append('x_{}'.format(i+1))
    obj_weight_value = 1.0   

    # Set the objectives. In this case: maximize value which is analogous as minimize the
    # same function with a minus in front.

    # Lineal objective
    lineal_objective = -obj_weight_value * quicksum(v[i] * bin_variables[i] 
                                                    for i in range(N))

    # Crossed-terms
    quadratic_objective = 0
    slice_counter = 0
    for i in range(N-1):
        quadratic_objective-=obj_weight_value * quicksum(
            vv[slice_counter + j] * bin_variables[i] * bin_variables[j] 
                                                    for j in range(N-1-i))
        slice_counter += 9-i


    # Add terms of objective function
    lineal_objective
    quadratic_objective
    objective = lineal_objective + quadratic_objective


    # Add the objective to the CQM
    cqm.set_objective(objective)

    # Set the constraints. In this case: maximum weight constraint
    cqm.add_constraint(quicksum(a[i]*bin_variables[i] for i in range(N)) <= b,
                        label = 'max_weight')


#######################################################################################
#                                  FROM CQM TO BQM                                    #
#######################################################################################
    bqm, invert = dimod.cqm_to_bqm(cqm)
    results = dimod.SimulatedAnnealingSampler().sample(bqm, num_reads=50)
    results_table = results.to_pandas_dataframe()[index_columns].sort_values(by=['energy'])
    results_table.to_csv('QKP_csv/{}.csv'.format(NAME))

    end = time.time()

    # Write RunTime to file
    file.write(NAME)
    file.write(' RunTime: ')
    file.write('{}'.format(end - start))
    file.write('(s)\n')
    print('RunTime: ', end - start)

#print('The total RunTime has been ', end, '(s)')
file.close()