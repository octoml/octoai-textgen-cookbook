import { Config } from "tailwindcss";
import defaultTheme from "tailwindcss/defaultTheme";

const theme: Config = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-orange": "linear-gradient(134deg, #FF6D57 0%, #FFA357 100%)",
        "gradient-teal": "linear-gradient(134deg, #0282FE 0%, #31D388 100%)",
        "gradient-light": "linear-gradient(180deg, #FFF 0%, #F7F7F7 100%)",
        "gradient-dark": "linear-gradient(180deg, #111213 0%, #000 100%)",
      },
      keyframes: {
        "pulse-full": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0" },
        },
        "fade-in": {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        "fade-out": {
          "0%": { opacity: "1" },
          "100%": { opacity: "0" },
        },
        "scale-in": {
          "0%": { opacity: "0", transform: "rotateX(-30deg) scale(0.9)" },
          "100%": { opacity: "1", transform: "rotateX(0deg) scale(1)" },
        },
        "scale-out": {
          "0%": { opacity: "1", transform: "rotateX(0deg) scale(1)" },
          "100%": { opacity: "0", transform: "rotateX(-10deg) scale(0.95)" },
        },
        "enter-from-right": {
          "0%": { opacity: "0", transform: "translateX(200px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
        "enter-from-left": {
          "0%": { opacity: "0", transform: "translateX(-200px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
        "exit-to-right": {
          "0%": { opacity: "1", transform: "translateX(0)" },
          "100%": { opacity: "0", transform: "translateX(200px)" },
        },
        "exit-to-left": {
          "0%": { opacity: "1", transform: "translateX(0)" },
          "100%": { opacity: "0", transform: "translateX(-200px)" },
        },
      },
      animation: {
        "pulse-full": "pulse-full 3s ease-in-out infinite",
        "fade-in": "fade-in 200ms ease",
        "fade-out": "fade-out 200ms ease",
        "scale-in": "scale-in 200ms ease",
        "scale-out": "scale-out 200ms ease",
        "enter-from-right": "enter-from-right 250ms ease",
        "enter-from-left": "enter-from-left 250ms ease",
        "exit-to-right": "exit-to-right 250ms ease",
        "exit-to-left": "exit-to-left 250ms ease",
      },
      spacing: {
        "9px": "0.5625rem",
      },
      transitionProperty: {
        "font-size": "font-size",
        spacing: "margin, padding, gap",
        sizing: "height, width",
      },
      invert: {
        "77": ".77",
        "100": "1",
      },
      sepia: {
        "4": ".04",
        "3": ".03",
      },
      saturate: {
        "194": "1.94",
        "103": "1.03",
      },
      hueRotate: {
        "145": "145deg",
        "136": "136deg",
      },
      brightness: {
        "84": ".84",
        "111": "1.11",
      },
      contrast: {
        "84": "84",
        "86": ".86",
      },
    },
    colors: {
      transparent: "transparent",
      white: "#FFFFFF",
      orange: "#FF6E57",
      blue: {
        100: "#B2DEFF",
        500: "#0096FF",
        700: "#1476DD",
        900: "#0D3B72",
      },
      black: {
        500: "#111213",
        600: "#0A0B0B",
        900: "#000000",
      },
      gray: {
        10: "#FAFAF9",
        25: "#F5F5F4",
        50: "#F7F7F7",
        100: "#EDEDED",
        200: "#E0E0E0",
        300: "#D0D1D2",
        400: "#9EA2A3",
        500: "#7B818A",
        600: "#6C707A",
        700: "#444950",
        800: "#34373C",
        900: "#1F2123",
      },
    },
    fontFamily: {
      sans: ["Lexend", ...defaultTheme.fontFamily.sans],
      display: ["Lexend", ...defaultTheme.fontFamily.sans],
      body: ["Lexend", ...defaultTheme.fontFamily.sans],
      smallcaps: ["Lexend", ...defaultTheme.fontFamily.sans],
    },
    fontSize: {
      "body-xs": [
        "0.75rem",
        {
          lineHeight: "1.25rem",
          fontWeight: 500,
        },
      ],
      "body-sm": [
        "0.875rem",
        {
          lineHeight: "1.25rem",
          fontWeight: 500,
        },
      ],
      body: [
        "1rem",
        {
          lineHeight: "1.375rem",
          fontWeight: 400,
          letterSpacing: "-.25px",
        },
      ],
      "2xs": [
        "1.25rem",
        {
          lineHeight: "1.75rem",
          fontWeight: 500,
          letterSpacing: "-.6px",
        },
      ],
      xs: [
        "1.5rem",
        {
          lineHeight: "2rem",
          fontWeight: 500,
          letterSpacing: "-.5px",
        },
      ],
      sm: [
        "1.625rem",
        {
          lineHeight: "1.875rem",
          fontWeight: 500,
          letterSpacing: "-.5px",
        },
      ],
      md: [
        "1.75rem",
        {
          lineHeight: "2.25rem",
          fontWeight: 500,
          letterSpacing: "-.85px",
        },
      ],
      lg: [
        "2rem",
        {
          lineHeight: "2.5rem",
          fontWeight: 500,
          letterSpacing: "-.65px",
        },
      ],
      xl: [
        "3rem",
        {
          lineHeight: "3.125rem",
          fontWeight: 500,
          letterSpacing: "-.95px",
        },
      ],
      "2xl": [
        "3.5rem",
        {
          lineHeight: "3.625rem",
          fontWeight: 500,
          letterSpacing: "-1.15px",
        },
      ],
    },
    boxShadow: {
      light: "0px 1px 10px 2px rgba(16, 24, 40, 0.05)",
      dark: "0px 1px 10px 2px rgba(255, 255, 255, 0.025)",
    },
  },
};

export default theme;
