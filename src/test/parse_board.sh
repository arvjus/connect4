#!/bin/bash

echo "board = np.array("
while read l; do
	echo $l | sed -e 's/ /,/g' -e 's/]$/],/g'
done
echo " np.int)"
