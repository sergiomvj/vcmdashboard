# VCM Dashboard - Simplified Dockerfile for Debugging
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies
RUN apk add --no-cache libc6-compat curl

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Accept build arguments
ARG VCM_SUPABASE_URL
ARG VCM_SUPABASE_ANON_KEY
ARG VCM_SUPABASE_SERVICE_ROLE_KEY
ARG OPENAI_API_KEY
ARG GOOGLE_AI_API_KEY

# Set environment variables for build
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV NEXT_PUBLIC_SUPABASE_URL=$VCM_SUPABASE_URL
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=$VCM_SUPABASE_ANON_KEY
ENV SUPABASE_SERVICE_ROLE_KEY=$VCM_SUPABASE_SERVICE_ROLE_KEY

# Build the application
RUN npm run build

# Debug: Show what was built
RUN echo "Build contents:" && ls -la .next/

# Expose port
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

# Add health check to help debug
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Start with debugging info
CMD ["sh", "-c", "echo 'Starting VCM Dashboard...' && echo 'Environment:' && env | grep -E '(NODE_|NEXT_|PORT|HOSTNAME)' && echo 'Starting npm...' && npm start"]