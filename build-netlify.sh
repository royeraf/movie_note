#!/bin/bash

# Build script for Netlify deployment
# This script prepares the serverless function by copying necessary files

echo "Building frontend..."
npm run build

echo "Preparing Netlify functions..."

# Copy the api directory to the function directory
echo "Copying API files..."
cp -r api netlify/functions/app/

# Copy requirements.txt to the function directory
echo "Copying requirements.txt..."
cp api/requirements.txt netlify/functions/

# Copy .env file if it exists (for local testing)
if [ -f .env ]; then
    echo "Note: Environment variables should be set in Netlify dashboard"
fi

echo "Build complete!"
