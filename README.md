# Data Simulation and Clustering Analysis

This project simulates data and performs clustering analysis using both R and Python. It generates simulated data for a range of covariance values (`cov_sim`), and then applies clustering analysis to the simulated data. Additionally, it evaluates the fits using various metrics.

## Usage

### Requirements

#### R
Ensure you have the following packages installed in R:
- `MASS`
- `flowClust`
- Any other dependent packages (e.g., `flowCore`)

#### Python
Ensure you have the following packages installed in Python:
- `numpy`
- `scikit-learn`

### How to Run

#### R

To run the R code, open the `R/simulate_and_cluster.R` file in your R environment and source it.

#### Python

To run the Python code, open the `Python/simulate_and_cluster.py` file and execute it in your Python environment.

### Code Explanation

#### R Code

```R
# Initialize lists to store fit models, KL divergences, and Z values for each kappa and cov_sim combination
fit_list2 <- list()
KL_mat2 <- list()
Z_mat2 <- list()
Z_mat5 <- list()
pi2 <- list()

# Loop over each cov_sim value in simulated_data_lists
for (cov_sim_name in names(simulated_data_lists)) {
  # Extract the list of simulated samples and their corresponding flow sims for the current cov_sim
  simulated_samples_for_cov_sim <- simulated_data_lists[[cov_sim_name]]$simulated_samples
  flow_sims_for_cov_sim <- simulated_data_lists[[cov_sim_name]]$flow_sims
  
  # Determine the number of simulations for the current cov_sim
  num_simulations_for_cov_sim <- length(simulated_samples_for_cov_sim)
  
  # Prepare sub-lists for storing results corresponding to the current cov_sim
  fit_list2[[cov_sim_name]] <- list()
  KL_mat2[[cov_sim_name]] <- matrix(0, nrow = num_simulations_for_cov_sim, ncol = length(Kappa_vals))
  Z_mat2[[cov_sim_name]] <- list()
  Z_mat5[[cov_sim_name]] <- list()
  pi2[[cov_sim_name]] <- list()  # Initialize the list for storing mixture weights for each kappa
  
  # Prepare the reference fit for the current cov_sim
  reference_fit <- flow_sims_for_cov_sim[[1]]  # Assuming the first simulation can serve as a reference
  toy_ref <- reference_fit
  toy_ref@sigma <- aperm(sigma, c(3, 2, 1))  # Adjust sigma dimensions if necessary
  toy_ref@mu <- t(mu)  # Transpose mu if necessary
  toy_ref@w <- pi  # Use the mixture weights from the first simulation as an example
  reference_fit <- toy_ref
  
  # Loop over kappa values
  for (i in 1:length(Kappa_vals)) {
    # Adjust the prior for each kappa value using the reference fit
    prior.sd1 <- Ghadeer2Prior(reference_fit, kappa = Kappa_vals[i])
    
    # Prepare sub-lists for storing results for the current kappa within the current cov_sim
    fit_list2[[cov_sim_name]][[i]] <- list()
    Z_mat2[[cov_sim_name]][[i]] <- list()
    Z_mat5[[cov_sim_name]][[i]] <- list()
    pi2[[cov_sim_name]][[i]] <- list()  # Prepare a sub-list for mixture weights for the current kappa
    
    for (j in 1:num_simulations_for_cov_sim) {
      # Print the current status
      print(paste("Processing cov_sim =", cov_sim_name, ", kappa =", Kappa_vals[i], "and simulation =", j))
      
      # Fit the model to the simulated sample
      secondary_fit <- flowClust(simulated_samples_for_cov_sim[[j]], K = 9, prior = prior.sd1, lambda = 1, trans = 0, usePrior = "yes")
      
      # Store the fit object and other metrics for each kappa, cov_sim, and sample combination
      fit_list2[[cov_sim_name]][[i]][[j]] <- secondary_fit
      KL_mat2[[cov_sim_name]][j, i] <- KLfun15(secondary_fit, reference_fit)
      Z_mat2[[cov_sim_name]][[i]][[j]] <- table(apply(secondary_fit@z, 1, which.max))
      Z_mat5[[cov_sim_name]][[i]][[j]] <- apply(secondary_fit@z, 1, which.max)
      pi2[[cov_sim_name]][[i]][[j]] <- secondary_fit@w  # Store mixture weights
    }
  }
}
