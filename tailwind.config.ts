import type { Config } from "tailwindcss";

export default {
    darkMode: ["class"],
    content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
  	extend: {
  		fontFamily: {
  			heading: ['var(--font-heading)', 'Playfair Display SC', 'serif'],
  			body: ['var(--font-body)', 'Karla', 'sans-serif'],
  		},
  		colors: {
  			background: 'hsl(var(--background))',
  			foreground: 'hsl(var(--foreground))',
  			card: {
  				DEFAULT: 'hsl(var(--card))',
  				foreground: 'hsl(var(--card-foreground))'
  			},
  			popover: {
  				DEFAULT: 'hsl(var(--popover))',
  				foreground: 'hsl(var(--popover-foreground))'
  			},
  			primary: {
  				DEFAULT: 'hsl(var(--primary))',
  				foreground: 'hsl(var(--primary-foreground))'
  			},
  			secondary: {
  				DEFAULT: 'hsl(var(--secondary))',
  				foreground: 'hsl(var(--secondary-foreground))'
  			},
  			muted: {
  				DEFAULT: 'hsl(var(--muted))',
  				foreground: 'hsl(var(--muted-foreground))'
  			},
  			accent: {
  				DEFAULT: 'hsl(var(--accent))',
  				foreground: 'hsl(var(--accent-foreground))'
  			},
  			destructive: {
  				DEFAULT: 'hsl(var(--destructive))',
  				foreground: 'hsl(var(--destructive-foreground))'
  			},
  			border: 'hsl(var(--border))',
  			input: 'hsl(var(--input))',
  			ring: 'hsl(var(--ring))',
  			chart: {
  				'1': 'hsl(var(--chart-1))',
  				'2': 'hsl(var(--chart-2))',
  				'3': 'hsl(var(--chart-3))',
  				'4': 'hsl(var(--chart-4))',
  				'5': 'hsl(var(--chart-5))'
  			},
  			gold: 'hsl(var(--gold))',
  			cream: 'hsl(var(--cream))',
  			terracotta: 'hsl(var(--terracotta))',
  			sand: 'hsl(var(--sand))',
  			dark: 'hsl(var(--dark))',
  		},
  		borderRadius: {
  			lg: 'var(--radius)',
  			md: 'calc(var(--radius) - 2px)',
  			sm: 'calc(var(--radius) - 4px)'
  		},
  		animation: {
  			'fade-in-up': 'fadeInUp 0.8s ease-out forwards',
  			'slide-in-left': 'slideInLeft 0.8s ease-out forwards',
  			'slide-in-right': 'slideInRight 0.8s ease-out forwards',
  		},
  		keyframes: {
  			fadeInUp: {
  				from: { opacity: '0', transform: 'translateY(30px)' },
  				to: { opacity: '1', transform: 'translateY(0)' },
  			},
  			slideInLeft: {
  				from: { opacity: '0', transform: 'translateX(-30px)' },
  				to: { opacity: '1', transform: 'translateX(0)' },
  			},
  			slideInRight: {
  				from: { opacity: '0', transform: 'translateX(30px)' },
  				to: { opacity: '1', transform: 'translateX(0)' },
  			},
  		},
  	}
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
