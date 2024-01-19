#!/bin/bash

PUBLISH_LOC="aivo@people.cyber.ee:public_html/mkdocs_try1"

echo "<!DOCTYPE html><html><body>" > index.html

for doc in cdoc2-system-usecasemodel cdoc2-proto-crypto-spec cdoc2-system-architecture; do 
    (cd $doc; mkdocs build; rsync -r site/* "${PUBLISH_LOC}/${doc}")
    echo "<a href=\"$doc/\">$doc</a><p>" >> index.html
done

echo "</body></html>" >> index.html

rsync index.html "${PUBLISH_LOC}"



