#!/bin/bash
# running all experiments automatically

./01_prepare_environment.sh
./02_experiment_kg_creation.sh
./03_experiment_validation.sh
./04_experiment_querying.sh
./05_plots.sh
./06_clean_environment.sh
