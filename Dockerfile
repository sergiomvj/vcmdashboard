# VCM Dashboard - Production Ready Dockerfile
FROM node:20-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    libc6-compat \
    curl

# Accept build arguments
ARG VCM_SUPABASE_URL
ARG VCM_SUPABASE_ANON_KEY

# Set environment variables for production
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV NEXT_PUBLIC_SUPABASE_URL=$VCM_SUPABASE_URL
ENV NEXT_PUBLIC_SUPABASE_ANON_KEY=$VCM_SUPABASE_ANON_KEY

# Copy package files first for better caching
COPY vcm-dashboard-real/package*.json ./

# Install dependencies with frozen lockfile
RUN npm ci --only=production --no-audit

# Copy source code
COPY vcm-dashboard-real/ ./

# Build the application
RUN npm run build

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Change ownership of the .next directory
USER nextjs

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:80/api/health || exit 1
# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:80/api/health || exit 1

# Use Next.js optimized start command
CMD ["npm", "start"]