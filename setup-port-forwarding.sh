#!/bin/bash
ssh -L localhost:2005:prd-gsm:2005 \
    -L localhost:2011:prd-gsm:2011 \
    sdehaan@prd-txtalert-gateway.44st.prk-host.net \
    -t 
