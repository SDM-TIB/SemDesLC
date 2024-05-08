#!/bin/bash

redir localhost:8890 kg_lc:8890
sbt -Dsbt.task.timings=true "run --endpoint http://localhost:8890/sparql --schema /shapes/shapes-LC.ttl --engine shaclex" | tail -n 250 | sed -nr "s/^.*Total time: (\S+) ms.*$/\1/p"
