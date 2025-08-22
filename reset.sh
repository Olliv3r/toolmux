#!/usr/bin/env bash
#
#

dir=.
tp="d"
nm="__pycache__"

text="Removendo cache do Python"

r=$(find $dir -type "$tp" -name "$nm" -exec rm -rf {} +)

echo "Removendo cache do python..."

if [ -n "$r" ]; then
	echo "$text...OK"

elif [ -z "$r" ]; then
	echo "$text...Already"

else
	echo "$text...Failed"
fi
