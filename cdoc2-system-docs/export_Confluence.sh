#!/bin/bash

source "$HOME/.confluence_password.bash"

#M2C_BIN="$HOME/tmp/repos/CDOC2/markmd-upload-to-confluence/mark"
M2C_BIN="$HOME/tmp/repos/CDOC2/mark/mark"


RIA_CONFLUENCE_URL="https://confluence.ria.ee/"
RIA_CONFLUENCE_SPACE="IB"
#RIA_CONFLUENCE_GRANDPARENT="mkDocsTesting"
#--parents-delimiter "/" --parents "${RIA_CONFLUENCE_GRANDPARENT}/DOCS-${CURRENT_REPO_TAG}"

CURRENT_REPO_TAG=$(git describe --tags)

$M2C_BIN --debug --trace -u $RIA_CONFLUENCE_USERNAME -p $RIA_CONFLUENCE_PASSWORD -b $RIA_CONFLUENCE_URL -f "docs/01_use_case_model/ch02_business_cases.md" --space $RIA_CONFLUENCE_SPACE --title-from-h1 --drop-h1 || exit 1;

exit 1

PAGES="01_use_case_model/ch02_business_cases.md 01_use_case_model/ch03_use_cases.md 02_protocol_and_cryptography_spec/ch02_encryption_schemes.md"

for page in $PAGES; do 
    echo $page
    $M2C_BIN --debug --trace -u $RIA_CONFLUENCE_USERNAME -p $RIA_CONFLUENCE_PASSWORD -b $RIA_CONFLUENCE_URL -f "docs/$page" --space $RIA_CONFLUENCE_SPACE   --title-from-h1 --drop-h1 || exit 1;
done


