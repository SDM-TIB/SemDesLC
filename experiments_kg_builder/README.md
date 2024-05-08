# SemDesLC: KG Builder Experiments

## Requirements
### Machine Requirements
- OS: Ubuntu 16.04.6 LTS or newer
- Memory: 64+ GiB
- HDD: approx. 5 GiB free disk space

### Software
- Docker - v19.03.6 or newer
- docker-compose - v1.26.0 or newer

### Bash Commands
The experiment scripts use the following bash commands:

- chown
- echo
- logname
- sed
- sleep

## Experiments
In order to facilitate the reproduction of the results, all components are encapsulated in Docker containers and the experiments are controlled via Shell scripts.
You can run the entire pipeline by executing:
```bash
sudo ./00_auto.sh
```

In the following, the different scripts are described in short.

- _00_auto.sh_: Executes the entire experiment automatically
- _01_prepare_environment.sh_: Prepares the experimental environment, i.e., sets up the Docker containers
- _03_experiment_validation.sh_: Executes the experiments for KG Validation
- _04_experiment_querying.sh_: Executes the experiments for Federated Query Evaluation
- _05_plots.sh_: Creates the plots presented in the paper
- _06_clean_environment.sh_: Cleans up the experimental environment including changing the ownership of result files to the user executing the script
