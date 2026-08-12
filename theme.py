"""Spot color palette and typography."""

LIGHT_COLORS = {
    'bg': '#FAF8FF',
    'card': '#FFFFFF',
    'card_hover': '#E8EAF8',

    'sidebar': '#F2F3FF',
    'sidebar_hover': '#E8EAF8',
    'sidebar_active': '#FF7A00',

    'input_bg': '#F9FAFB',
    'popup_bg': '#FFFFFF',

    'border': '#E5E7EB',
    'border_light': '#D3D5E0',

    'primary': '#FF7A00',
    'primary_hover': '#E56D00',

    'secondary': '#00A3FF',
    'secondary_hover': '#008EDB',

    'success': '#2EB872',
    'warning': '#FF7A00',
    'danger': '#E53935',
    'info': '#00A3FF',

    'stat_total': '#00A3FF',
    'stat_lost': '#E53935',
    'stat_lent': '#FF7A00',
    'stat_borrowed': '#2EB872',

    'text': '#1A1B21',
    'text_muted': '#6B7280',
    'text_dark': '#4B4D57',
    'text_inverse': '#FFFFFF',
}


DARK_COLORS = {
    'bg': '#111318',
    'card': '#1B1E26',
    'card_hover': '#252934',

    'sidebar': '#181B22',
    'sidebar_hover': '#252934',
    'sidebar_active': '#FF7A00',

    'input_bg': '#20232B',
    'popup_bg': '#1B1E26',

    'border': '#30343D',
    'border_light': '#3A3E48',

    'primary': '#FF7A00',
    'primary_hover': '#E56D00',

    'secondary': '#00A3FF',
    'secondary_hover': '#008EDB',

    'success': '#2EB872',
    'warning': '#FF7A00',
    'danger': '#E53935',
    'info': '#00A3FF',

    'stat_total': '#00A3FF',
    'stat_lost': '#E53935',
    'stat_lent': '#FF7A00',
    'stat_borrowed': '#2EB872',

    'text': '#F5F5F7',
    'text_muted': '#A5A8B2',
    'text_dark': '#D5D7DE',
    'text_inverse': '#FFFFFF',
}


# Current theme
DARK_MODE = False

COLORS = LIGHT_COLORS.copy()


def toggle_dark_mode():
    """Switch between light and dark mode."""

    global DARK_MODE, COLORS

    DARK_MODE = not DARK_MODE

    if DARK_MODE:
        COLORS.clear()
        COLORS.update(DARK_COLORS)
    else:
        COLORS.clear()
        COLORS.update(LIGHT_COLORS)

    return DARK_MODE


def set_dark_mode(enabled):
    """Set dark mode explicitly."""

    global DARK_MODE, COLORS

    DARK_MODE = enabled

    COLORS.clear()

    if DARK_MODE:
        COLORS.update(DARK_COLORS)
    else:
        COLORS.update(LIGHT_COLORS)


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
 