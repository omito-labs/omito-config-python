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