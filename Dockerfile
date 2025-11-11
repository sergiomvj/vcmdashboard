# VCM Dashboard - Hybrid Dockerfile with Python Backend Support
FROM node:20-alpine

WORKDIR /app

# Install system dependencies including Python
RUN apk add --no-cache \
    libc6-compat \
    curl \
    python3 \
    py3-pip \
    python3-dev \
    build-base

# Create symlink for python command
RUN ln -sf python3 /usr/bin/python

# Accept build arguments
ARG VCM_SUPABASE_URL
ARG VCM_SUPABASE_ANON_KEY

# Set environment variables
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV NEXT_PUBLIC_SUPABASE_URL=$VCM_SUPABASE_URL
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=$VCM_SUPABASE_ANON_KEY

# Copy Python requirements and install Python dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt || echo "No Python requirements found - continuing with mock mode"

# Copy package files first
COPY vcm-dashboard-real/package*.json ./

# Install ALL dependencies (including devDependencies for build)
RUN npm install --include=dev

# Copy all source files
COPY vcm-dashboard-real/ ./

# Copy Python automation scripts (optional - will enable full functionality if present)
COPY AUTOMACAO/ ../AUTOMACAO/ || echo "No AUTOMACAO folder found - using mock mode"

# Build the application
RUN npm run build

EXPOSE 3000

# Health check
HEALTHCHECK CMD curl -f http://localhost:3000/api/health || exit 1

# Use the correct command for standalone build
CMD ["node", ".next/standalone/server.js"]