# Fujitsu Interview Technical Test - Solve Two well-known Combinatorial Optimization Problems
**Author**: *Sergio López Baños*
## Files in current folder
- Two Jupyter Notebooks with the solutions to the problems suggested.
- Two Python scripts that loop over the .txt file to generate the .csv files (solutions).
- QAP_csv: .csv of QAP instances.
- QKP_csv: .csv of QKP instances.
- requirements.txt: Manual text file that contain the neccesary Python packages to solve the problems.
- extended_requirements.txt: The .txt produced by ´pip freeze > extended_requirements.txt´
## Solvers
- I know that these problems could be solved using the real quantum annealer from D-Wave but I do not have a premium account and the monthly 1min from the annealer is destinated to my master thesis. For that reason I am not going to use the real quantum annealer.
- The laptop I used to solve the assignment was a MacBook Pro M1 13 Inch.
## Summary of approach ideas of both problems
- For sure, I do NOT want to solve each problem by hand, by formulating the qubo and then filling the matrix with loops (slow and bad approach) or using numpy (just bad approach numpy vectorize works faster than loops)
- I need to read the data of the .txt files (Pandas comes handy for this) taking care of what represent each data (eg. the second coefficient correspond to x2 and so on). When reading the document I need to be careful with blank lines or comments (that does not represent a coefficient). The data is gonna be stored in list or numpy arrays (does no matter as can converts list to arrays easily).
- **Idea 1** *(Pedagogical Approach)*: Looking at the Hamiltonian of our problem I can add the Penalties to it (Lagrange multipliers) and then with the QUBO objective function I can multiply the numpy arrays accordingly to produce the QUBO matrix (this is fast because numpy call C and C++ libraries). After that I can use some sampler from D-Wave (e.g. exact sampler for small instances or simulatedannealing for large instances) to solve the problem by inserting the QUBO matrix Q. 
CONS: This approach is horrible if the problem I am tackling has many variables since taking into account the constraints into the Hamiltonian and re-written it by hand becomes almost impossible ("You should do this at least once in live for a small problem").
- **Idea 2** *(Not that bad)*: Instead of re-writting the constraints as penalties in the Hamiltonian I can use the BinaryQuadraticModel from D-Wave to take into account the constraints in the model (D-Wave does the work) so that I only need to take care of formulating the QUBO matrix of the objective function (without the constraints) and then add_linear_inequality_constraint (analogously with equality constraints).
CONS: It is true that I save time not formulating the QUBO problem by adding the penalty terms but I have to write down the objective function which could be a problem if we have too many variables.
- **Idea 3** *(CQM)*: It is similar to the previous approach but it allows me to code the problem even faster. I can write the problem using the CQM class, then for large instances I can translate CQM to BQM using the cqm_to_bqm method so that I can insert the bqm model in the SimulatedAnnealingSampler.
- **Idea 4** *Tabu search*: If I want to fix the time I can use the tabu sampler that has the timeout parameter (useful for large instance where we do not have a hint about the optimal solution or the penalty value).

## Final thoughts
Thanks for giving me the opportunity to solve this two combinatorial optimization problems. I have to admit that I had already knowledge about the knapsack problem but I did not know its quadratic version so I thanks you for teaching me this flavour (in linux lingo) of the knapsack problem. <br>
Finally, I list what I have learnt:
- Working with numpy matrices that store objects. Pros: It is easy to formulate the problem via CQM. Cons: If we deal with large matrices of objects the calculations are slow (Is there any way of improving it?)(Maybe adding as decorator the quicksum() from dimod so that numpy producs add terms according to quicksum() instead of np.sum()). <br>
- I knew that there are two class os SimulatedAnnealingSampler (from dimod and neal packages), however I learnt by doing this project that the one from neal is faster. <br>
- BQM allows you to formulate the problem for larger instances faster (better RunTime) than CQM. In order to limit the amount of execution time for each instance I use the tabu sampler (it has a timeout parameters to fix the execution time. After that time it outputs the best result found.) <br>
- On one hand, QAP is solved by constructing a function call QAP_problem() so I am building the "black box" to be called during the execution. On the other hand, in the QKP problem I decide not to build a function that encapsulate the problem formulation (despite this can be done easily).

I really enjoy the assignments and I hope that we can have a fruitful discussion of the notebooks.






