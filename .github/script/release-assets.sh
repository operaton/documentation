#!/usr/bin/env bash

# Copyright 2025 the Operaton contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Script to collect release assets from GitHub repository operaton/operaton to build directory
DOWNLOAD_DIR="download"

CLEAR=0
VERBOSE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --clear|-c)
      CLEAR=1
      shift
      ;;
    --verbose|-v)
      VERBOSE=1
      shift
      ;;
    *)
      shift
      ;;
  esac
done

if [[ $CLEAR -eq 1 ]]; then
  echo "Deleting $DOWNLOAD_DIR..."
  rm -rf "$DOWNLOAD_DIR"
fi

mkdir -p "$DOWNLOAD_DIR"

ASSETS=(
  "javadoc.zip"
  "rest-api.zip"
  "clirr-reports.zip"
)

# Get a list of releases from GitHub API using gh
RELEASES_JSON=$(gh api repos/operaton/operaton/releases --jq '.[] | {tag_name: .tag_name, assets: .assets}')

# Loop through each release name, search for assets, and download them
for RELEASE in $(echo "$RELEASES_JSON" | jq -c '.'); do
  TAG_NAME=$(echo "$RELEASE" | jq -r '.tag_name')
  echo "Processing release: $TAG_NAME"

  for ASSET_NAME in "${ASSETS[@]}"; do
    ASSET_URL=$(echo "$RELEASE" | jq -r --arg NAME "$ASSET_NAME" '.assets[] | select(.name == $NAME) | .url')
    ASSET_FILE="$DOWNLOAD_DIR/${TAG_NAME}/${ASSET_NAME}"

    if [[ -n "$ASSET_URL" ]]; then
      if [[ -f "$ASSET_FILE" ]]; then
        echo "  Asset $ASSET_NAME from release $TAG_NAME already exists, skipping download."
      else
        mkdir -p $DOWNLOAD_DIR/${TAG_NAME}
        echo "  Downloading asset $ASSET_NAME from release $TAG_NAME"
        gh api "$ASSET_URL" --header 'Accept: application/octet-stream' > "$ASSET_FILE"
      fi
    else
      if [[ $VERBOSE -eq 1 ]]; then
        echo "  Asset $ASSET_NAME not found in release $TAG_NAME"
      fi
    fi
  done
done

# After download, process all zip files in DOWNLOAD_DIR.
# Unpack them in a subdir with the name of the zip file without extension. Then delete the zip file.
for ZIP_FILE in $(find $DOWNLOAD_DIR -type f -name "*.zip"); do
  BASE_NAME=$(basename "$ZIP_FILE" .zip)
  ASSET_DIR="build/reference/$(basename $(dirname "$ZIP_FILE"))/$BASE_NAME"

  if [[ $CLEAR -eq 1 ]]; then
    echo "Deleting $ASSET_DIR..."
    rm -rf "$ASSET_DIR"
  fi

  mkdir -p "$ASSET_DIR"
  echo "Unzipping $ZIP_FILE to $ASSET_DIR"
  unzip -q "$ZIP_FILE" -d "$ASSET_DIR"
done
echo "✅ Done!"
