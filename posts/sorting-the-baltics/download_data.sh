#!/bin/bash

LATEST_VERSION=48.1
wget https://unicode.org/Public/cldr/$LATEST_VERSION/cldr-common-$LATEST_VERSION.zip
unzip cldr-common-$LATEST_VERSION.zip "common/main/*" -d cldr-data
