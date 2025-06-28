#!/bin/bash

echo "📦 Installing Project-002..."

# Make launcher executable
chmod +x project-002

# Copy or link to /usr/local/bin for global access
sudo ln -sf "$(pwd)/project-002" /usr/local/bin/project-002

echo "✅ Installed! Run with: project-002"
