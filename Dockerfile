# VCM Dashboard - Fixed Dockerfile
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

# Clean any existing build and build fresh
RUN rm -rf .next && npm run build

# Debug: Show what was built
RUN echo "Build contents:" && ls -la .next/

# Expose port (but let Easypanel control the actual port)
EXPOSE 3000

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-3000}/ || exit 1

# Use dynamic port from environment, fallback to 3000
CMD ["sh", "-c", "echo 'Starting VCM Dashboard on port '${PORT:-3000}'...' && echo 'Environment:' && env | grep -E '(NODE_|NEXT_|PORT)' && npx next start -p ${PORT:-3000}"]