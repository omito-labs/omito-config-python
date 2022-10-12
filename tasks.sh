#! /usr/bin/env bash

# @describe omito config tasks
# @author barathvk@gmail.com

# @cmd bump versions
# @flag --force force the version bump for all packages
version() {
  dirs=$(ls -d -- */)
  for dir in $dirs; do
    package=$(echo ${dir} | sed 's:/*$::')
    changes=$(git status --porcelain ${package})
    if [ -z "$changes" ] && [ ! ${argc_force} ]; then
      pushd ./${package} > /dev/null
      echo "no changes to package ${package} [$(poetry version --short)]"
      popd > /dev/null
    else
      echo "[[package ${package}]]"
      pushd ./${package} > /dev/null
      poetry version patch
      popd > /dev/null
    fi
  done
}

eval $(argc "$0" "$@")