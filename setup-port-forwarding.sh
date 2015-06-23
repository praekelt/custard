#!/bin/bash
ssh -L localhost:2001:prd-gsm:2001 banele@prd-txtalert-gateway.44st.prk-host.net -t top
