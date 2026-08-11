"""Spot color palette and typography."""

COLORS = {
    # Core interface
    'bg': '#FAF8FF',
    'sidebar': '#F2F3FF',
    'sidebar_hover': '#E8EAF8',
    'sidebar_active': '#FF7A00',

    # Cards and surfaces
    'card': '#FFFFFF',
    'card_hover': '#F9FAFB',
    'input_bg': '#F9FAFB',
    'popup_bg': '#FFFFFF',

    # Borders
    'border': '#E5E7EB',
    'border_light': '#E5E7EB',

    # Primary
    'primary': '#FF7A00',
    'primary_hover': '#E56D00',

    # Secondary
    'secondary': '#00A3FF',
    'secondary_hover': '#008EDB',

    # Status
    'success': '#2EB872',
    'warning': '#FF7A00',
    'danger': '#E53935',
    'info': '#00A3FF',

    # Stat cards
    'stat_total': '#00A3FF',
    'stat_lost': '#E53935',
    'stat_lent': '#FF7A00',
    'stat_borrowed': '#2EB872',

    # Text
    'text': '#1A1B21',
    'text_muted': '#6B7280',
    'text_dark': '#4B5563',
    'text_inverse': '#FFFFFF',
}


FONTS = {
    'logo': ('Segoe UI', 20, 'bold'),
    'title': ('Segoe UI', 20, 'bold'),
    'heading': ('Segoe UI', 13, 'bold'),

    'body': ('Segoe UI', 10),
    'body_bold': ('Segoe UI', 10, 'bold'),

    'small': ('Segoe UI', 9),
    'small_bold': ('Segoe UI', 9, 'bold'),

    'button': ('Segoe UI', 10, 'bold'),
    'badge': ('Segoe UI', 8, 'bold'),
}


STATUS_COLORS = {
    'stored': '#2EB872',
    'available': '#2EB872',
    'lent': '#FF7A00',
    'borrowed': '#00A3FF',
    'lost': '#E53935',
    'overdue': '#E53935',
}


BREAKPOINTS = {
    'xs': 0,
    'sm': 700,
    'md': 900,
    'lg': 1100,
    'xl': 1400,
}


 