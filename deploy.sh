#!/bin/bash
# Deploy MPK Mini IV Remote files to Reason

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/reason_remote"

# Reason Remote locations on macOS (user library)
REMOTE_BASE="$HOME/Library/Application Support/Propellerhead Software/Remote"
CODECS_DIR="$REMOTE_BASE/Codecs/Lua Codecs/Akai"
MAPS_DIR="$REMOTE_BASE/Maps/Akai"

echo "Deploying MPK Mini IV Remote files..."
echo ""

# Clean up old directories with wrong case
rm -rf "$REMOTE_BASE/Maps/AKAI" 2>/dev/null
rm -rf "$REMOTE_BASE/Codecs/Lua Codecs/AKAI" 2>/dev/null

# Create directories if they don't exist
mkdir -p "$CODECS_DIR"
mkdir -p "$MAPS_DIR"

# Copy codec files
cp "$SOURCE_DIR/MPK mini IV.luacodec" "$CODECS_DIR/"
cp "$SOURCE_DIR/MPK mini IV.lua" "$CODECS_DIR/"

# Copy map file
cp "$SOURCE_DIR/MPK_mini_IV.remotemap" "$MAPS_DIR/MPK mini IV.remotemap"

echo "Deployed:"
echo "  -> $CODECS_DIR/MPK mini IV.luacodec"
echo "  -> $CODECS_DIR/MPK mini IV.lua"
echo "  -> $MAPS_DIR/MPK mini IV.remotemap"
echo ""

# Verify
echo "Verifying deployment..."
ls -la "$CODECS_DIR/"
echo ""
ls -la "$MAPS_DIR/"
echo ""
echo "Restart Reason to load the new Remote files."
