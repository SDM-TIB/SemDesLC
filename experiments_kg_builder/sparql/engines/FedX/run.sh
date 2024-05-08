#!/bin/bash

redir localhost:8890 kg_lc:8890
redir localhost:8891 kg_semdeslc:8890
echo -n "$1,"; java -Xmx16g -Dlog4j.configuration=file:log4j.properties -cp bin:./lib/* com.fluidops.fedx.CLI -logtofile -d endpoints.fedx @q /queries/$1.sparql | tail -n 3 | sed -nr "s/^.*duration=(\S+)ms.*results=(\S+).*$/\1,\2/p"; echo ""
