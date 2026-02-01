#!/bin/bash

# Build script for Netlify deployment
# This script prepares the serverless function by copying necessary files

echo "Building frontend..."
npm run build

echo "Preparing Netlify functions..."

# Copy the api directory to the functions directory (not app subdirectory)
echo "Copying API files..."
rm -rf netlify/functions/api
cp -r api netlify/functions/

# The requirements.txt is already in netlify/functions/
echo "Requirements.txt is ready"

# Copy .env file if it exists (for local testing)
if [ -f .env ]; then
    echo "Note: Environment variables should be set in Netlify dashboard"
fi

echo "Build complete!"
