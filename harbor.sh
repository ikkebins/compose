#!/bin/bash
HARBOR_URL="https://xxxxxxxx"
SRCPROJECT="ocp"
SRCREPO="openshift%252Frelease"
REPOSRC="openshift%2Frelease"
USER="xxxxxxxxx"
PASSWORD="xxxxxxxxxxx"
DESTPROJECT="openshift"
DESTREPO="myrelease"



PAGE=1
PAGE_SIZE=1  

while :; do
    RESPONSE=$(curl -s -u "$USER:$PASSWORD" "$HARBOR_URL/api/v2.0/projects/$SRCPROJECT/repositories/$SRCREPO/artifacts?page=$PAGE&page_size=$PAGE_SIZE")

    # Falls keine Artefakte mehr zurückkommen, breche ab
    if [[ "$RESPONSE" == "[]" ]]; then
        break
    fi

    DIGEST=$(echo "$RESPONSE" | jq -r '.[].digest | sub("sha256:"; "sha256%3A")')
    
    printf "%s\n" $DIGEST

    #kopieren

    curl -s -u "$USER:$PASSWORD" -X 'POST' "$HARBOR_URL/api/v2.0/projects/$DESTPROJECT/repositories/$DESTREPO/artifacts?from=$SRCPROJECT%2F$REPOSRC%40$DIGEST"
    #printf "Return :%s\n" $RET


    ((PAGE++))
done
