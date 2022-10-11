#! /usr/bin/env bash

# @describe omito config tasks
# @author barathvk@gmail.com

# @cmd bump versions
version() {
  dirs=$(ls -d -- */)
  for dir in $dirs; do
    package=$(echo ${dir} | sed 's:/*$::')
    changes=$(git status --porcelain ${package})
    if [ -z "$changes" ]; then
      echo "no changes to package ${package}"
    else
      echo "bumping version for package ${package}"
      pushd ./${package}
      poetry version patch
      popd
    fi
  done
}

eval $(argc "$0" "$@")