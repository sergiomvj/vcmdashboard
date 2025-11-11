# VCM Dashboard - Maximum Debug Dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies first
RUN apk add --no-cache libc6-compat curl

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

# Debug: Check package.json
RUN echo "=== PACKAGE.JSON CHECK ===" && cat package.json && echo "=== END PACKAGE.JSON ==="

# Install dependencies
RUN npm install --verbose

# Copy all source files
COPY vcm-dashboard-real/ ./

# Debug: Check what files we have
RUN echo "=== FILES CHECK ===" && \
    ls -la && \
    echo "=== SRC STRUCTURE ===" && \
    find src -type f -name "*.ts" -o -name "*.tsx" | head -20 && \
    echo "=== ENV VARIABLES ===" && \
    env | grep -E "(NODE|NEXT|VCM)" && \
    echo "=== DEBUG END ==="

# Try to run Next.js build with maximum debug
RUN echo "=== STARTING BUILD ===" && \
    npx next build --debug || \
    (echo "=== BUILD FAILED - DETAILED DEBUG ===" && \
     echo "Node version:" && node --version && \
     echo "NPM version:" && npm --version && \
     echo "Next.js installation:" && npm list next && \
     echo "TypeScript check:" && npx tsc --noEmit --skipLibCheck || echo "TypeScript check failed" && \
     echo "ESLint check:" && npx eslint --version || echo "ESLint not found" && \
     echo "Directory contents:" && ls -la .next || echo "No .next directory" && \
     exit 1)

EXPOSE 3000

# Simple health check
HEALTHCHECK CMD curl -f http://localhost:3000/api/health || exit 1

# Start the application
CMD ["npm", "start"]