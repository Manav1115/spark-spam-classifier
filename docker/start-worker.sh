#!/bin/bash

if [ -z "$SPARK_MASTER" ]; then
  echo "Error: SPARK_MASTER environment variable is not set."
  exit 1
fi

${SPARK_HOME}/sbin/start-worker.sh ${SPARK_MASTER}
tail -f ${SPARK_HOME}/logs/*
