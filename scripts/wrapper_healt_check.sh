#!/bin/bash
# health_check_wrapper.sh - Wrapper script for health check

#!/bin/bash

# The Alcyoneus DB - Health Check Wrapper
# Version: 4.1.0

ALCY_HOME="/data/data/com.termux/files/home/Alcy"
LOG_FILE="$ALCY_HOME/logs/health_check.log"
DB_PATH="$ALCY_HOME/data/platforms.json"
REPORT_PATH="$ALCY_HOME/reports"

# Create directories if not exist
mkdir -p "$ALCY_HOME/logs"
mkdir -p "$REPORT_PATH"

# Function to run health check
run_health_check() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting health check..." >> "$LOG_FILE"
    
    python3 "$ALCY_HOME/validation/health_check.py" --check --db "$DB_PATH" >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Health check completed successfully" >> "$LOG_FILE"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Health check failed with error code $?" >> "$LOG_FILE"
    fi
}

# Function to get health stats
get_stats() {
    python3 "$ALCY_HOME/validation/health_check.py" --stats --db "$DB_PATH"
}

# Function to verify single platform
verify_platform() {
    platform=$1
    python3 "$ALCY_HOME/validation/health_check.py" --verify "$platform" --db "$DB_PATH"
}

# Command line interface
case "$1" in
    run)
        run_health_check
        ;;
    stats)
        get_stats
        ;;
    verify)
        verify_platform "$2"
        ;;
    daemon)
        python3 "$ALCY_HOME/validation/health_check.py" --daemon --db "$DB_PATH"
        ;;
    *)
        echo "Usage: $0 {run|stats|verify <platform>|daemon}"
        exit 1
        ;;
esac
