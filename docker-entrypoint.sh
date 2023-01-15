#!/bin/bash
curl https://tunnel.pyjam.as/8002 > tunnel.conf
wg-quick up ./tunnel.conf
uvicorn app.main:app --host 0.0.0.0 --port 8002