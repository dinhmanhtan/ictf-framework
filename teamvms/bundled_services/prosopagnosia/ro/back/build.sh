#!/usr/bin/env bash

set -uex

make --jobs=9
cp prosopagnosia ..
strip ../prosopagnosia

