#!/usr/bin/env bash
set -euo pipefail

state=$(eww windows | grep dashboard)

if [ "$state" == "*dashboard" ]; then
    eww close dashboard
else
    eww open dashboard
fi
