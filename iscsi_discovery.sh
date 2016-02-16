#!/bin/bash
iscsiadm -m discovery -t st -p 172.26.13.110:3260
iscsiadm -m node -l 
