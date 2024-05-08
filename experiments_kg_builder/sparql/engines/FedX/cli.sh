#!/bin/bash
java -Xmx16g -Dlog4j.configuration=file:log4j.properties -cp bin:./lib/* com.fluidops.fedx.CLI $*
