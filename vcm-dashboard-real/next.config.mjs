/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker
  output: 'standalone',
  
  // Disable x-powered-by header for security
  poweredByHeader: false,
  
  // ESLint configuration for production builds
  eslint: {
    ignoreDuringBuilds: true,
  },
  
  // TypeScript configuration for production builds
  typescript: {
    ignoreBuildErrors: true,
  },
  
  // Optimize images
  images: {
    unoptimized: true, // Better for containers
  },
  
  // Optimize images
  images: {
    unoptimized: true, // Better for containers
  },
  
  // Disabled experimental features for stability
  experimental: {
    optimizeCss: false,
    webpackBuildWorker: false,
  },
  
  // Webpack optimizations
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };
    }
    return config;
  },
};

export default nextConfig;
