# Entropology
Appendices, support code for analysis and figures discussed in: Paula Gheorghiade, Vaiva Vasiliauskaite, Aleksandr Diachenko, Henry Price, Tim Evans, Ray Rivers (2023). Entropology: an information-theoretic approach to understanding archaeological data. Journal of Archaeological Method and Theory. 

## Data
The included dataset has been collected as part of Gheorghiade, P. (2020). “A Network Approach to Interaction and Maritime Connectivity on Crete during the Late Bronze Age – Late Minoan II-IIIB2.” Doctoral Thesis, University of Toronto. It has been modified for this specific paper. See Notes section for how we organized and used the data in this paper.

## Entropology Code 
diversity_calculators.py - includes functions for calculating sample diversity, gamma diversity, alpha diversity, beta diversity and similarity:

utilities.py - utility functions for opening and pre-processing the data (read_df), plotting beta diversity (run_beta) , alpha_diversity (run_alpha) , gamma_diversity (run_gamma and run_gamma_error where the latter plots gamma diversity with errors, obtained by bootstrapping the samples), as well as plotting individual sites' diversity (run_site_error, where the diversity is plotted with errors, obtained by bootstrapping the samples)

## Figures
The figures folder includes generated figures. The folder "Entropology_Dataset_Flattened/Solo_Period" includes figures presented in the paper. In the subfolder "Solo_Period_Include_LMIIIA_LMIIIB" we present results where data from LM III A is included in LM IIIA1 and LM III B is included in LM IIIB1.  

All figures were generated using the following scripts:
fig3_notebook.py - to plot figure 3 of the paper
entropologyTable2.py - to plot figure 7 of the paper
figure_plotter.py - the main file for generating the rest of the figures presented in the paper

# References
If you use this code, please cite latest version (1.3):
<a href="https://doi.org/10.5281/zenodo.8101056"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.8101056.svg" alt="DOI"></a>
<br>
<br>
Link to the preprint of the [paper](https://www.researchsquare.com/article/rs-2686626/v1). 
<br>
<br>




