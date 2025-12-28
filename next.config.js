/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'hebbkx1anhila5yf.public.blob.vercel-storage.com',
      },
      {
        protocol: 'https',
        hostname: '06jfzz4maekxll04.public.blob.vercel-storage.com',
      },
      {
        protocol: 'https',
        hostname: 'www.ganjingworld.com',
      },
    ],
  },
};

module.exports = nextConfig;

