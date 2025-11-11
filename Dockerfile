# VCM Dashboard - Ultra Simple Dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies first
RUN apk add --no-cache libc6-compat

# Accept build arguments
ARG VCM_SUPABASE_URL
ARG VCM_SUPABASE_ANON_KEY

# Set environment variables
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV NEXT_PUBLIC_SUPABASE_URL=$VCM_SUPABASE_URL
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=$VCM_SUPABASE_ANON_KEY

# Copy package files and install
COPY vcm-dashboard-real/package*.json ./
RUN npm install

# Copy all source files
COPY vcm-dashboard-real/ ./

# Build with more verbose output and error handling
RUN echo "Starting build..." && \
    npm run build || (echo "Build failed! Here's what we have:" && ls -la && echo "Package.json:" && cat package.json && exit 1)

EXPOSE 3000

# Simple health check
HEALTHCHECK CMD curl -f http://localhost:3000/api/health || exit 1

# Start the application
CMD ["npm", "start"]