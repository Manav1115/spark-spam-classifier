#!/bin/bash
${SPARK_HOME}/sbin/start-master.sh -h 0.0.0.0
tail -f ${SPARK_HOME}/logs/*
