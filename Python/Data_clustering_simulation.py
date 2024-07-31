import numpy as np
from sklearn.mixture import GaussianMixture
import warnings

# Assume simulated_data_lists, Kappa_vals, mu, sigma, pi, and other necessary variables are defined

# Initialize lists to store fit models, KL divergences, and Z values for each kappa and cov_sim combination
fit_list2 = {}
KL_mat2 = {}
Z_mat2 = {}
Z_mat5 = {}
pi2 = {}

# Loop over each cov_sim value in simulated_data_lists
for cov_sim_name in simulated_data_lists.keys():
    # Extract the list of simulated samples and their corresponding flow sims for the current cov_sim
    simulated_samples_for_cov_sim = simulated_data_lists[cov_sim_name]['simulated_samples']
    flow_sims_for_cov_sim = simulated_data_lists[cov_sim_name]['flow_sims']
    
    # Determine the number of simulations for the current cov_sim
    num_simulations_for_cov_sim = len(simulated_samples_for_cov_sim)
    
    # Prepare sub-lists for storing results corresponding to the current cov_sim
    fit_list2[cov_sim_name] = []
    KL_mat2[cov_sim_name] = np.zeros((num_simulations_for_cov_sim, len(Kappa_vals)))
    Z_mat2[cov_sim_name] = []
    Z_mat5[cov_sim_name] = []
    pi2[cov_sim_name] = []  # Initialize the list for storing mixture weights for each kappa
    
    # Prepare the reference fit for the current cov_sim
    reference_fit = flow_sims_for_cov_sim[0]  # Assuming the first simulation can serve as a reference
    
    # Loop over kappa values
    for i, kappa in enumerate(Kappa_vals):
        # Adjust the prior for each kappa value using the reference fit
        prior_sd1 = Ghadeer2Prior(reference_fit, kappa=kappa)
        
        # Prepare sub-lists for storing results for the current kappa within the current cov_sim
        fit_list2[cov_sim_name].append([])
        Z_mat2[cov_sim_name].append([])
        Z_mat5[cov_sim_name].append([])
        pi2[cov_sim_name].append([])
        
        for j in range(num_simulations_for_cov_sim):
            print(f"Processing cov_sim = {cov_sim_name}, kappa = {kappa}, and simulation = {j}")
            
            try:
                secondary_fit = GaussianMixture(n_components=9, covariance_type='full').fit(simulated_samples_for_cov_sim[j])
                
                fit_list2[cov_sim_name][i].append(secondary_fit)
                KL_mat2[cov_sim_name][j, i] = KLfun15(secondary_fit, reference_fit)
                Z_mat2[cov_sim_name][i].append(np.bincount(secondary_fit.predict(simulated_samples_for_cov_sim[j])))
                Z_mat5[cov_sim_name][i].append(secondary_fit.predict(simulated_samples_for_cov_sim[j]))
                pi2[cov_sim_name][i].append(secondary_fit.weights_)
            except Exception as e:
                warnings.warn(f"Clustering failed for simulation {j}: {e}")
