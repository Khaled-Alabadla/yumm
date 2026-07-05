tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
        colors: {
            primary:  { DEFAULT: '#B5451B', dark: '#9A3A16', light: '#FDF0EB' },
            surface:  { DEFAULT: '#ffffff', dark: '#1E1E1E' },
            bg:       { DEFAULT: '#F7F7F7', dark: '#141414' },
            border:   { DEFAULT: '#E8E8E8', dark: '#2A2A2A' },
            muted:    { DEFAULT: '#6B7280', dark: '#9CA3AF' },
        },
        fontFamily: {
            display: ['Tajawal', 'Inter', 'system-ui', 'sans-serif'],
            sans:    ['Inter', 'Tajawal', 'system-ui', 'sans-serif'],
            tajawal: ['Tajawal', 'sans-serif'],
        },
        borderRadius: { '2xl': '1rem', '3xl': '1.5rem', '4xl': '2rem' },
        boxShadow: {
            card:        '0 2px 16px rgba(0,0,0,.07)',
            'card-hover':'0 12px 40px rgba(0,0,0,.13)',
            primary:     '0 8px 24px rgba(181,69,27,.35)',
        },
        }
    }
}