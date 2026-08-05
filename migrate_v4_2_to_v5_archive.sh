#!/bin/bash

# ==========================================================
# Stock Quant Project
# v4.2 -> v5.0 migration
#
# Phase 1:
# Archive historical files
#
# IMPORTANT:
# This script DOES NOT DELETE anything.
# It only moves old versions into archive/
#
# ==========================================================


set -e


PROJECT_ROOT=$(pwd)

ARCHIVE_DIR="$PROJECT_ROOT/archive"

LOG_FILE="$PROJECT_ROOT/migration_v4_2_archive.log"


echo "========================================" | tee "$LOG_FILE"
echo "Stock v4.2 Archive Migration" | tee -a "$LOG_FILE"
echo "Project: $PROJECT_ROOT" | tee -a "$LOG_FILE"
echo "Time: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"


mkdir -p "$ARCHIVE_DIR/backtest"
mkdir -p "$ARCHIVE_DIR/strategy"
mkdir -p "$ARCHIVE_DIR/scripts"
mkdir -p "$ARCHIVE_DIR/debug"
mkdir -p "$ARCHIVE_DIR/tests"


move_file(){

    SRC=$1
    DST=$2


    if [ -f "$SRC" ]; then

        mkdir -p "$(dirname "$DST")"

        if [ -e "$DST" ]; then

            echo "[SKIP] target exists: $DST" | tee -a "$LOG_FILE"

        else

            mv "$SRC" "$DST"

            echo "[MOVE] $SRC -> $DST" | tee -a "$LOG_FILE"

        fi

    else

        echo "[MISS] $SRC" | tee -a "$LOG_FILE"

    fi
}



echo ""
echo "---- Archive backtest history ----"


move_file \
"backtest/engine_v2.py" \
"archive/backtest/engine_v2.py"


move_file \
"backtest/engine_v3.py" \
"archive/backtest/engine_v3.py"


move_file \
"backtest/report_v1.py" \
"archive/backtest/report_v1.py"


move_file \
"backtest/report_v2.py" \
"archive/backtest/report_v2.py"


move_file \
"backtest/benchmark_v1.py" \
"archive/backtest/benchmark_v1.py"


move_file \
"backtest/risk.py" \
"archive/backtest/risk.py"



echo ""
echo "---- Archive old strategy ----"


move_file \
"strategy/macd.py" \
"archive/strategy/macd.py"


move_file \
"strategy/ma_cross.py" \
"archive/strategy/ma_cross.py"



echo ""
echo "---- Archive old scripts ----"


move_file \
"scripts/build_stock_pool_v1.py" \
"archive/scripts/build_stock_pool_v1.py"


move_file \
"scripts/download_daily.py" \
"archive/scripts/download_daily.py"


move_file \
"scripts/download_daily_raw_all.py" \
"archive/scripts/download_daily_raw_all.py"


move_file \
"scripts/download_financial_all.py" \
"archive/scripts/download_financial_all.py"



echo ""
echo "---- Archive debug files ----"


if [ -d "debug_export" ]; then

    mv debug_export archive/debug/

    echo "[MOVE] debug_export -> archive/debug/" \
    | tee -a "$LOG_FILE"

fi



if [ -d "debug_snapshot" ]; then

    mv debug_snapshot archive/debug/

    echo "[MOVE] debug_snapshot -> archive/debug/" \
    | tee -a "$LOG_FILE"

fi



echo ""
echo "---- Archive temporary tests ----"


move_file \
"tests/t1.py" \
"archive/tests/t1.py"



echo ""
echo "========================================"
echo "Migration finished."
echo ""
echo "Please run:"
echo ""
echo "git status"
echo ""
echo "Then test:"
echo ""
echo "python -m pytest"
echo ""
echo "========================================"


echo "Finished: $(date)" >> "$LOG_FILE"
