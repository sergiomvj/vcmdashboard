# VCM Dashboard - FIXED Dockerfile with correct start command
FROM node:20-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache libc6-compat curl

# Accept build arguments
ARG VCM_SUPABASE_URL
ARG VCM_SUPABASE_ANON_KEY

# Set environment variables
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV NEXT_PUBLIC_SUPABASE_URL=$VCM_SUPABASE_URL
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=$VCM_SUPABASE_ANON_KEY

# Copy package files first
COPY vcm-dashboard-real/package*.json ./

# Install ALL dependencies (including devDependencies for build)
RUN npm install --include=dev

# Copy all source files
COPY vcm-dashboard-real/ ./

# Build the application
RUN npm run build

EXPOSE 3000

# Health check
HEALTHCHECK CMD curl -f http://localhost:3000/api/health || exit 1

# Use the correct command for standalone build
CMD ["node", ".next/standalone/server.js"]