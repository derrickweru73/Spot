"""Dark Ocean color palette and typography for Spot."""

COLORS = {
    'bg': '#0B1120',
    'sidebar': '#0F172A',
    'sidebar_hover': '#162032',
    'sidebar_active': '#1E293B',
    'card': '#1E293B',
    'card_hover': '#27354F',
    'input_bg': '#0F172A',
    'popup_bg': '#151E32',
    'border': '#334155',
    'border_light': '#475569',
    'primary': '#2DD4BF',
    'primary_hover': '#14B8A6',
    'secondary': '#FB7185',
    'secondary_hover': '#F43F5E',
    'success': '#34D399',
    'warning': '#FBBF24',
    'danger': '#F87171',
    'info': '#60A5FA',
    'text': '#F8FAFC',
    'text_muted': '#94A3B8',
    'text_dark': '#64748B',
    'text_inverse': '#0F172A',
}

FONTS = {
    'logo': ('Segoe UI', 20, 'bold'),
    'title': ('Segoe UI', 18, 'bold'),
    'heading': ('Segoe UI', 13, 'bold'),
    'body': ('Segoe UI', 10),
    'body_bold': ('Segoe UI', 10, 'bold'),
    'small': ('Segoe UI', 9),
    'small_bold': ('Segoe UI', 9, 'bold'),
    'button': ('Segoe UI', 10, 'bold'),
    'badge': ('Segoe UI', 8, 'bold'),
}

STATUS_COLORS = {
    'stored': '#34D399',
    'available': '#34D399',
    'lent': '#FBBF24',
    'borrowed': '#60A5FA',
    'lost': '#F87171',
    'overdue': '#F87171',
}

BREAKPOINTS = {
    'xs': 0,
    'sm': 700,
    'md': 900,
    'lg': 1100,
    'xl': 1400,
}


# --- TEST BLOCK (remove after testing) ---
# if __name__ == "__main__":
#     print("Theme loaded!")
#     print("Background color:", COLORS['bg'])
#     print("Primary color:", COLORS['primary'])
#     print("Title font:", FONTS['title'])
#     print("Success status:", STATUS_COLORS['stored'])
#     print("Mobile breakpoint:", BREAKPOINTS['md'], "px")feat