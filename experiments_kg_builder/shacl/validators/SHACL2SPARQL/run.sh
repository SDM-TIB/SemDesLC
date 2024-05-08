#!/bin/bash

java -Xmx16G -jar valid-1.0-SNAPSHOT.jar -r -d /shapes http://kg_lc:8890/sparql ./result | tail -n 1 | sed -nr "s/^.*Total execution time: (\S+).*$/\1/p"
