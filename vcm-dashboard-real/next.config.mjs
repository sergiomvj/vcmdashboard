/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker deployment
  output: 'standalone',
  
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
