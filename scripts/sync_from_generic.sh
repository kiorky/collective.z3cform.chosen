#!/usr/bin/env bash
cd $(dirname $0)/..
PROJECT="collective.z3cform.chosen"
IMPORT_URL="https://github.com/kiorky/collective.js.chosen"
cd $(dirname $0)/..
[[ ! -d t ]] && mkdir t
rm -rf t/*
tar xzvf $(ls -1t ~/cgwb/$PROJECT*z|head -n1) -C t
files="
./
"
rm -rf t/src/collective/z3cform/chosen/dashboard.py
rm -rf t/src/collective/z3cform/chosen/static
rm -rf t/scripts
for f in $files;do
    rsync -aKzv --exclude="sync_from_generic.sh"  t/$PROJECT/$f $f
done
rm -rf src/collective/z3cform/chosen/dashboard.py
rm -rf src/collective/z3cform/chosen/static 
# vim:set et sts=4 ts=4 tw=80:
