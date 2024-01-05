import designSystem from '@octoml/design-system/tailwind.config';

import type { Config } from 'tailwindcss';

const config: Config = {
    content: [
        './node_modules/@octoml/design-system/dist/**/*.js',
        './src/**/*.{js,jsx,ts,tsx}',
        './app/**/*.{js,ts,jsx,tsx}'
    ],
    presets: [designSystem],
    darkMode: 'class',
    plugins: [],
    theme: {
        extend: {
            fontSize: {
                'dsc-lg': '1.875rem',
                'hd-lg': '3.75rem'
            },
            height: {
                '55vh': '55vh'
            },
            spacing: {
                '80px': '5rem',
                '160px': '10rem',
                '300px': '18.75rem',
                '35vh': '35vh'
            },
            maxWidth: {
                container: '1780px'
            },
            backgroundColor: {
                'dark-gray': '#111213'
            },
            backgroundImage: {
                noise: "url('/images/noise.png')",
                'gradient-blk-to-btm-l':
                    'linear-gradient(0deg, #111213 0%, rgba(17, 18, 19, 0.00) 37.07%)',
                'gradient-blk-to-top-r':
                    'linear-gradient(20deg, #111213 0.6%, rgba(17, 18, 19, 0.00) 82.95%)',
                'gradient-blk-to-l':
                    'linear-gradient(80deg, #111213 16.09%, rgba(17, 18, 19, 0.00) 47.02%)',
                'gradient-blk-to-r':
                    'linear-gradient(260deg, #111213 7.24%, rgba(17, 18, 19, 0.00) 55.34%)',
                'gradient-blk-to-btm':
                    'linear-gradient(180deg, rgba(29, 30, 31, 5) 50%, rgba(29, 30, 31, 0) 100%)'
            },
            opacity: {
                65: '.65'
            },
            transitionProperty: {
                spacing: 'margin, padding, gap',
                size: 'width, height',
                font: 'font-size, line-height'
            },
            screens: {
                'desktop-lg': '1470px',
                'desktop-xl': '1600px'
            }
        }
    }
};
export default config;
