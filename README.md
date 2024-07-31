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

The R script `simulate_and_cluster.R` initializes lists to store fit models, KL divergences, and Z values for each kappa and cov_sim combination. It loops over each `cov_sim` value in `simulated_data_lists`, extracting the list of simulated samples and their corresponding flow sims for the current `cov_sim`. It then fits the model to the simulated sample and stores the fit object and other metrics.

#### Python Code

The Python script `simulate_and_cluster.py` follows a similar process. It initializes lists to store fit models, KL divergences, and Z values for each kappa and cov_sim combination. It loops over each `cov_sim` value in `simulated_data_lists`, extracting the list of simulated samples and their corresponding flow sims for the current `cov_sim`. It then fits the model to the simulated sample using `GaussianMixture` from `scikit-learn` and stores the fit object and other metrics.

## Contribution

We welcome contributions to improve the project. Please open issues or submit pull requests on GitHub.

## License

This project is part of a student project at Trinity College Dublin. For more details, see the `LICENSE` file.
