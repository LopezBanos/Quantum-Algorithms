import os
import numpy as np
import pandas as pd
import dimod
import neal
import tabu
from dimod import ConstrainedQuadraticModel,BinaryQuadraticModel, Binary, quicksum

def QAP_problem(path, skip):
    """
    Function that formulate the bqm model depending on the data it read.
    Args:
        path: Path to file
        skip: kwarg
    """
#=======================================================================================#
#                        Working with dre.txt files                                     #
#=======================================================================================#
    if skip==1:
        # Problem size
        S = int(pd.read_csv(path, delim_whitespace=True, 
                            nrows=1, 
                            header=None).iloc[0].to_list()[0])

        # Flow Matrix
        F = pd.read_csv(path, skiprows=skip, delim_whitespace=True,
                        nrows=S, 
                        header=None).to_numpy()

        # Distance Matrix
        D = pd.read_csv(path, skiprows=S+skip+1, delim_whitespace=True, 
                        nrows=S, header=None).to_numpy()

        # Convert to matrix
        D = np.asmatrix(D)
        F = np.asmatrix(F)

    #######################################################################################
    #                                    BUILD THE BQM                                    #
    #######################################################################################
        # Build the BQM
        bqm = BinaryQuadraticModel('BINARY') # Initialize the BQM
        # For loops are not fast but they are faster than numpy matrix multiplication with dtype=objects
        for i in range(S):
            for j in range(S):
                for p in range(S):
                    for q in range(S):
                        # Cannot have diagonal terms
                        if (i==j) and (p==q):
                            continue
                            #bqm.add_linear('x_{}_{}'.format(i+1,p+1), F[i,i]*D[p,p]) # Zero term in diagonals
                        else:
                            bqm.add_quadratic('x_{}_{}'.format(i+1,p+1),'x_{}_{}'.format(j+1,q+1), F[i,j]*D[p,q])

    #######################################################################################
    #                                    CONSTRAINTS                                      #
    #######################################################################################
        # Optimal Value
        first_line = pd.read_csv(path, delim_whitespace=True, nrows=1, header=None).iloc[0].to_list()
        if len(first_line)==2:
            optimal = first_line[1]
        else:
            optimal = 10e6

        # First Constraints
        for row in range(S):
            constraint = [('x_{}_{}'.format(row+1,j+1), 1) for j in range(S)]
            bqm.add_linear_equality_constraint(
                constraint,
                constant = -1,
                lagrange_multiplier = 4*optimal)
            
        # Second Constraints
        for column in range(S):
            constraint = [('x_{}_{}'.format(i+1,column+1), 1) for i in range(S)]
            bqm.add_linear_equality_constraint(
                constraint,
                constant = -1,
                lagrange_multiplier = 4*optimal)
            
#=======================================================================================#
#                        Working with tai.txt files                                     #
#=======================================================================================#
    if skip==2:
        # Problem size
        S = int(pd.read_csv(path, delim_whitespace=True, 
                            nrows=1, 
                            header=None).iloc[0].to_list()[0])
        # Flow Matrix
        F = pd.read_csv(path, skiprows=skip, delim_whitespace=True, nrows=S, header=None).to_numpy()
        F_T = F.T

        # Distance Matrix
        D = pd.read_csv(path, skiprows=S+skip+1, delim_whitespace=True, nrows=S, header=None).to_numpy()

        # Create X matrix
        X = np.empty([S,S],dtype=object)
        for i in range(S):
            for j in range(S):
                X[i,j] = Binary('x_{}_{}'.format(i+1,j+1))
        X[X == None] = 0
        X = np.asmatrix(X)

    #######################################################################################
    #                                    BUILD THE CQM                                    #
    #######################################################################################
        # Build the CQM
        cqm = ConstrainedQuadraticModel()

        # Matrix Multiplication (not to fast for large matrices)
        B = X@(D@X.T)
        objective = quicksum(F_T[diag,j]*B[j,diag] for diag in range(S) for j in range(S))

        # Add the objective to the CQM
        cqm.set_objective(objective)

    #######################################################################################
    #                                    CONSTRAINTS                                      #
    #######################################################################################
        for i in range(S):
            cqm.add_constraint(quicksum(X[i,j] for j in range(S)) == 1)
        for j in range(S):
            cqm.add_constraint(quicksum(X[i,j] for i in range(S)) == 1)

    #######################################################################################
    #                                  FROM CQM TO BQM                                    #
    #######################################################################################
        bqm, invert = dimod.cqm_to_bqm(cqm)            
    return bqm


def path_for_any_os(folder, file_name):
    '''
    A function gives the path for the instances for any system.
    Args:
        file_name: (str) Name of the file we want to read. 
    '''
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    file_path = os.path.join(parent_directory, 'instances', folder, file_name)
    return file_path

def total_number_binary_variables(size):
    '''
    A function that outputs the total number of binary variables
    for a two_index to single_index mapping.
    Args:
        S: (int) Problem size.
    '''
    total = 0
    for i in range(1,size):
        total+= (size - i)
    return total

# Mapping from two-indexes to single-index
def k(i, j, N):
    '''
    A function that map two indexes "i" and "j" to a single index "k"
    for a given problem size "N".
    Args:
        N: (int) Problem size. 
        i: (int) Index.
        j: (int) Index.
    '''
    # Undefined
    if i==j:
        pass
    # k(j,i,N)
    if i>j:
        aux = i
        i = j
        j = aux
        single_index = i*N - i*(N-1)/2 + j - (i+1)
    # Single Index
    if i<j:
        single_index = i*N - i*(N-1)/2 + j - (i+1)
    return int(single_index)