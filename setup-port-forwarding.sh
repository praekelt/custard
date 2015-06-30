#!/bin/bash
ssh -L localhost:2002:prd-gsm:2002 \
    -L localhost:2011:prd-gsm:2011 \
    "$@"@prd-txtalert-gateway.44st.prk-host.net \
    -t 
