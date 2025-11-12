/** @type {import('next').NextConfig} */
const nextConfig = {
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
    domains: ['localhost'],
    unoptimized: process.env.NODE_ENV === 'development'
  },
  
  // Enable experimental features for better performance
  experimental: {
    // Enable modern build optimizations
    optimizeCss: true,
    // Improve cold start performance
    webpackBuildWorker: true,
  },
  
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
