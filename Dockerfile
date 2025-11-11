# VCM Dashboard - Dockerfile with Standalone Output
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies
RUN apk add --no-cache libc6-compat

# Copy package files
COPY package*.json ./

# Install only production dependencies initially
RUN npm ci --only=production && npm cache clean --force

# Install dev dependencies for build
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

# Build the application (generates standalone output)
RUN npm run build

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy the standalone output and set permissions
RUN cp -r .next/standalone/* . && \
    cp -r .next/static .next/ && \
    cp -r public . && \
    chown -R nextjs:nodejs /app

# Clean up build artifacts to reduce image size
RUN rm -rf .next/cache node_modules/.cache

# Switch to non-root user  
USER nextjs

# Expose port
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

# Start the application using standalone server
CMD ["node", "server.js"]