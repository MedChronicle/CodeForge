import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#080a13',
        panel: '#111426',
        panelSoft: '#171b31',
        violet: '#8b5cf6',
        cyan: '#22d3ee',
        mint: '#34d399',
        coral: '#fb7185',
        amber: '#fbbf24',
      },
      fontFamily: {
        display: ['Space Grotesk', 'ui-sans-serif', 'system-ui'],
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
      boxShadow: {
        neon: '0 0 36px rgba(139, 92, 246, 0.25)',
        cyan: '0 0 32px rgba(34, 211, 238, 0.2)',
      },
      backgroundImage: {
        mesh: 'radial-gradient(circle at 15% 20%, rgba(139,92,246,.22), transparent 32%), radial-gradient(circle at 85% 15%, rgba(34,211,238,.16), transparent 28%), radial-gradient(circle at 58% 85%, rgba(52,211,153,.1), transparent 30%)',
      },
      borderRadius: {
        '4xl': '2rem',
      },
    },
  },
  plugins: [],
} satisfies Config;
