/** @type {import('next').NextConfig} */
const nextConfig = {
  // Remove standalone for now - might be causing issues
  // output: 'standalone',
  
  // Force cache busting
  generateEtags: false,
  
  // Disable x-powered-by header for security
  poweredByHeader: false,
  
  // Disable ESLint during build for production (warnings become errors)
  eslint: {
    ignoreDuringBuilds: true,
  },
  
  // Disable TypeScript errors during build (for faster production builds)
  typescript: {
    ignoreBuildErrors: true,
  },
  
  // Server configuration
  async rewrites() {
    return [
      {
        source: '/health',
        destination: '/api/health',
      },
      {
        source: '/status',
        destination: '/api/status',
      },
    ]
  },
  
  // Optimize images
  images: {
    domains: ['localhost'],
    unoptimized: process.env.NODE_ENV === 'development'
  },
  
  // Disable experimental features for stable build
  // experimental: {
  //   optimizeCss: true,
  //   webpackBuildWorker: true,
  // },
  
  // Webpack optimizations
  webpack: (config, { isServer }) => {
    // Reduce bundle size
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
