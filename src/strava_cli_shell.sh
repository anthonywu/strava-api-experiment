#!/bin/bash

if [ -z "$STRAVA_API_TOKEN" ]; then
  ./strava_local_client.py find_settings
  ./strava_local_client.py -h
else
  konch
fi
