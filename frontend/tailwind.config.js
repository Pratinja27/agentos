export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        serif: ["Fraunces", "Times New Roman", "serif"],
        sans: ["IBM Plex Sans", "Segoe UI", "sans-serif"],
        mono: ["IBM Plex Mono", "Consolas", "monospace"],
      },
      colors: {
        ink: "#1b1a16",
        paper: "#f3ece0",
        card: "#fffaf2",
        moss: "#24362c",
        clay: "#c45c26",
        sage: "#4d6b58",
      },
    },
  },
};
