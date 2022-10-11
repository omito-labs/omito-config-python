#! /usr/bin/env bash

# @describe omito config tasks
# @author barathvk@gmail.com

# @cmd bump versions
version() {
  dirs=$(ls -d -- */)
  for file in $dirs; do
    package=$(echo $file | sed 's:/*$::')
    echo "bumping version for package ${package}"
  done
}

eval $(argc "$0" "$@")