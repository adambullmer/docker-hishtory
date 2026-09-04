#!/usr/bin/env python3
"""
Generate all 22 shadcn theme CSS files for hiSHtory webserver.
Supports light/dark mode via prefers-color-scheme media queries.
Overrides Bootstrap 5.3.2 variables & components.
"""

import os

THEMES_DIR = os.path.join(os.path.dirname(__file__), "..", "root", "usr", "share", "hishtory", "themes")
os.makedirs(THEMES_DIR, exist_ok=True)

BASES = {
    "zinc": {
        "light": {
            "bg": "#ffffff", "bg_rgb": "255, 255, 255",
            "fg": "#09090b", "fg_rgb": "9, 9, 11",
            "border": "#e4e4e7", "muted": "#f4f4f5", "hover": "#f4f4f5",
            "header_bg": "#18181b", "header_fg": "#fafafa"
        },
        "dark": {
            "bg": "#09090b", "bg_rgb": "9, 9, 11",
            "fg": "#f4f4f5", "fg_rgb": "244, 244, 245",
            "border": "#27272a", "muted": "#18181b", "hover": "#27272a",
            "header_bg": "#18181b", "header_fg": "#fafafa"
        }
    },
    "slate": {
        "light": {
            "bg": "#ffffff", "bg_rgb": "255, 255, 255",
            "fg": "#020817", "fg_rgb": "2, 8, 23",
            "border": "#e2e8f0", "muted": "#f1f5f9", "hover": "#f1f5f9",
            "header_bg": "#0f172a", "header_fg": "#f8fafc"
        },
        "dark": {
            "bg": "#020817", "bg_rgb": "2, 8, 23",
            "fg": "#f8fafc", "fg_rgb": "248, 250, 252",
            "border": "#1e293b", "muted": "#0f172a", "hover": "#1e293b",
            "header_bg": "#0f172a", "header_fg": "#f8fafc"
        }
    },
    "stone": {
        "light": {
            "bg": "#ffffff", "bg_rgb": "255, 255, 255",
            "fg": "#0c0a09", "fg_rgb": "12, 10, 9",
            "border": "#e7e5e4", "muted": "#f5f5f4", "hover": "#f5f5f4",
            "header_bg": "#1c1917", "header_fg": "#fafaf9"
        },
        "dark": {
            "bg": "#0c0a09", "bg_rgb": "12, 10, 9",
            "fg": "#fafaf9", "fg_rgb": "250, 250, 249",
            "border": "#292524", "muted": "#1c1917", "hover": "#292524",
            "header_bg": "#1c1917", "header_fg": "#fafaf9"
        }
    },
    "gray": {
        "light": {
            "bg": "#ffffff", "bg_rgb": "255, 255, 255",
            "fg": "#030712", "fg_rgb": "3, 7, 18",
            "border": "#e5e7eb", "muted": "#f3f4f6", "hover": "#f3f4f6",
            "header_bg": "#111827", "header_fg": "#f9fafb"
        },
        "dark": {
            "bg": "#030712", "bg_rgb": "3, 7, 18",
            "fg": "#f9fafb", "fg_rgb": "249, 250, 251",
            "border": "#1f2937", "muted": "#111827", "hover": "#1f2937",
            "header_bg": "#111827", "header_fg": "#f9fafb"
        }
    },
    "neutral": {
        "light": {
            "bg": "#ffffff", "bg_rgb": "255, 255, 255",
            "fg": "#0a0a0a", "fg_rgb": "10, 10, 10",
            "border": "#e5e5e5", "muted": "#f5f5f5", "hover": "#f5f5f5",
            "header_bg": "#171717", "header_fg": "#fafafa"
        },
        "dark": {
            "bg": "#0a0a0a", "bg_rgb": "10, 10, 10",
            "fg": "#fafafa", "fg_rgb": "250, 250, 250",
            "border": "#262626", "muted": "#171717", "hover": "#262626",
            "header_bg": "#171717", "header_fg": "#fafafa"
        }
    }
}

THEMES = {
    "lime": {"base": "zinc", "light_pri": "#84cc16", "light_pri_rgb": "132, 204, 22", "light_pri_fg": "#0f172a", "dark_pri": "#a3e635", "dark_pri_rgb": "163, 230, 53", "dark_pri_fg": "#0f172a"},
    "amber": {"base": "zinc", "light_pri": "#f59e0b", "light_pri_rgb": "245, 158, 11", "light_pri_fg": "#ffffff", "dark_pri": "#fbbf24", "dark_pri_rgb": "251, 191, 36", "dark_pri_fg": "#09090b"},
    "blue": {"base": "zinc", "light_pri": "#2563eb", "light_pri_rgb": "37, 99, 235", "light_pri_fg": "#ffffff", "dark_pri": "#3b82f6", "dark_pri_rgb": "59, 130, 246", "dark_pri_fg": "#ffffff"},
    "cyan": {"base": "zinc", "light_pri": "#0891b2", "light_pri_rgb": "8, 145, 178", "light_pri_fg": "#ffffff", "dark_pri": "#06b6d4", "dark_pri_rgb": "6, 182, 212", "dark_pri_fg": "#09090b"},
    "emerald": {"base": "zinc", "light_pri": "#059669", "light_pri_rgb": "5, 150, 105", "light_pri_fg": "#ffffff", "dark_pri": "#10b981", "dark_pri_rgb": "16, 185, 129", "dark_pri_fg": "#09090b"},
    "fuchsia": {"base": "zinc", "light_pri": "#c026d3", "light_pri_rgb": "192, 38, 211", "light_pri_fg": "#ffffff", "dark_pri": "#d946ef", "dark_pri_rgb": "217, 70, 239", "dark_pri_fg": "#ffffff"},
    "green": {"base": "zinc", "light_pri": "#16a34a", "light_pri_rgb": "22, 163, 74", "light_pri_fg": "#ffffff", "dark_pri": "#22c55e", "dark_pri_rgb": "34, 197, 94", "dark_pri_fg": "#09090b"},
    "indigo": {"base": "zinc", "light_pri": "#4f46e5", "light_pri_rgb": "79, 70, 229", "light_pri_fg": "#ffffff", "dark_pri": "#6366f1", "dark_pri_rgb": "99, 102, 241", "dark_pri_fg": "#ffffff"},
    "orange": {"base": "zinc", "light_pri": "#f97316", "light_pri_rgb": "249, 115, 22", "light_pri_fg": "#ffffff", "dark_pri": "#fb923c", "dark_pri_rgb": "251, 146, 60", "dark_pri_fg": "#09090b"},
    "pink": {"base": "zinc", "light_pri": "#db2777", "light_pri_rgb": "219, 39, 119", "light_pri_fg": "#ffffff", "dark_pri": "#f472b6", "dark_pri_rgb": "244, 114, 182", "dark_pri_fg": "#09090b"},
    "purple": {"base": "zinc", "light_pri": "#9333ea", "light_pri_rgb": "147, 51, 234", "light_pri_fg": "#ffffff", "dark_pri": "#a855f7", "dark_pri_rgb": "168, 85, 247", "dark_pri_fg": "#ffffff"},
    "red": {"base": "zinc", "light_pri": "#dc2626", "light_pri_rgb": "220, 38, 38", "light_pri_fg": "#ffffff", "dark_pri": "#ef4444", "dark_pri_rgb": "239, 68, 68", "dark_pri_fg": "#ffffff"},
    "rose": {"base": "zinc", "light_pri": "#e11d48", "light_pri_rgb": "225, 29, 72", "light_pri_fg": "#ffffff", "dark_pri": "#f43f5e", "dark_pri_rgb": "244, 63, 94", "dark_pri_fg": "#ffffff"},
    "sky": {"base": "zinc", "light_pri": "#0284c7", "light_pri_rgb": "2, 132, 199", "light_pri_fg": "#ffffff", "dark_pri": "#38bdf8", "dark_pri_rgb": "56, 189, 248", "dark_pri_fg": "#09090b"},
    "teal": {"base": "zinc", "light_pri": "#0d9488", "light_pri_rgb": "13, 148, 136", "light_pri_fg": "#ffffff", "dark_pri": "#14b8a6", "dark_pri_rgb": "20, 184, 166", "dark_pri_fg": "#09090b"},
    "violet": {"base": "zinc", "light_pri": "#7c3aed", "light_pri_rgb": "124, 58, 237", "light_pri_fg": "#ffffff", "dark_pri": "#8b5cf6", "dark_pri_rgb": "139, 92, 246", "dark_pri_fg": "#ffffff"},
    "yellow": {"base": "zinc", "light_pri": "#ca8a04", "light_pri_rgb": "202, 138, 4", "light_pri_fg": "#ffffff", "dark_pri": "#eab308", "dark_pri_rgb": "234, 179, 8", "dark_pri_fg": "#09090b"},
    "zinc": {"base": "zinc", "light_pri": "#18181b", "light_pri_rgb": "24, 24, 27", "light_pri_fg": "#fafafa", "dark_pri": "#fafafa", "dark_pri_rgb": "250, 250, 250", "dark_pri_fg": "#18181b"},
    "slate": {"base": "slate", "light_pri": "#0f172a", "light_pri_rgb": "15, 23, 42", "light_pri_fg": "#f8fafc", "dark_pri": "#f8fafc", "dark_pri_rgb": "248, 250, 252", "dark_pri_fg": "#0f172a"},
    "stone": {"base": "stone", "light_pri": "#1c1917", "light_pri_rgb": "28, 25, 23", "light_pri_fg": "#fafaf9", "dark_pri": "#fafaf9", "dark_pri_rgb": "250, 250, 249", "dark_pri_fg": "#1c1917"},
    "gray": {"base": "gray", "light_pri": "#111827", "light_pri_rgb": "17, 24, 39", "light_pri_fg": "#f9fafb", "dark_pri": "#f9fafb", "dark_pri_rgb": "249, 250, 251", "dark_pri_fg": "#111827"},
    "neutral": {"base": "neutral", "light_pri": "#171717", "light_pri_rgb": "23, 23, 23", "light_pri_fg": "#fafafa", "dark_pri": "#fafafa", "dark_pri_rgb": "250, 250, 250", "dark_pri_fg": "#171717"},
}

TEMPLATE = """/* ==============================================================================
 * hiSHtory Theme: {title} (Ported from shadcn/ui)
 * Supports automatic Light/Dark mode via prefers-color-scheme media queries
 * Overrides Bootstrap 5.3.2 CSS variables & UI components
 * ============================================================================== */

:root {{
  color-scheme: light;

  /* Theme Core Tokens (Light Mode) */
  --theme-primary: {light_pri};
  --theme-primary-rgb: {light_pri_rgb};
  --theme-primary-fg: {light_pri_fg};
  --theme-bg: {l_bg};
  --theme-bg-rgb: {l_bg_rgb};
  --theme-fg: {l_fg};
  --theme-fg-rgb: {l_fg_rgb};
  --theme-border: {l_border};
  --theme-muted: {l_muted};
  --theme-hover: {l_hover};
  --theme-header-bg: {l_header_bg};
  --theme-header-fg: {l_header_fg};

  /* Bootstrap 5.3 Core Variable Overrides */
  --bs-primary: var(--theme-primary);
  --bs-primary-rgb: var(--theme-primary-rgb);
  --bs-body-bg: var(--theme-bg);
  --bs-body-bg-rgb: var(--theme-bg-rgb);
  --bs-body-color: var(--theme-fg);
  --bs-body-color-rgb: var(--theme-fg-rgb);
  --bs-border-color: var(--theme-border);
  --bs-secondary-bg: var(--theme-muted);
  --bs-tertiary-bg: var(--theme-hover);
  --bs-link-color: var(--theme-primary);
  --bs-link-hover-color: var(--theme-primary);
  --bs-focus-ring-color: rgba(var(--theme-primary-rgb), 0.35);
}}

@media (prefers-color-scheme: dark) {{
  :root {{
    color-scheme: dark;

    /* Theme Core Tokens (Dark Mode) */
    --theme-primary: {dark_pri};
    --theme-primary-rgb: {dark_pri_rgb};
    --theme-primary-fg: {dark_pri_fg};
    --theme-bg: {d_bg};
    --theme-bg-rgb: {d_bg_rgb};
    --theme-fg: {d_fg};
    --theme-fg-rgb: {d_fg_rgb};
    --theme-border: {d_border};
    --theme-muted: {d_muted};
    --theme-hover: {d_hover};
    --theme-header-bg: {d_header_bg};
    --theme-header-fg: {d_header_fg};

    /* Bootstrap 5.3 Core Variable Overrides */
    --bs-primary: var(--theme-primary);
    --bs-primary-rgb: var(--theme-primary-rgb);
    --bs-body-bg: var(--theme-bg);
    --bs-body-bg-rgb: var(--theme-bg-rgb);
    --bs-body-color: var(--theme-fg);
    --bs-body-color-rgb: var(--theme-fg-rgb);
    --bs-border-color: var(--theme-border);
    --bs-secondary-bg: var(--theme-muted);
    --bs-tertiary-bg: var(--theme-hover);
    --bs-link-color: var(--theme-primary);
    --bs-link-hover-color: var(--theme-primary);
    --bs-focus-ring-color: rgba(var(--theme-primary-rgb), 0.35);
  }}
}}

/* ------------------------------------------------------------------------------
 * Base Page & Typography Styling
 * ------------------------------------------------------------------------------ */
html, body {{
  background-color: var(--bs-body-bg) !important;
  color: var(--bs-body-color) !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  transition: background-color 0.2s ease, color 0.2s ease;
  min-height: 100vh;
}}

/* ------------------------------------------------------------------------------
 * Header / Jumbotron Banner (.bg-secondary.text-white)
 * ------------------------------------------------------------------------------ */
.bg-secondary.text-white {{
  background-color: var(--theme-header-bg) !important;
  color: var(--theme-header-fg) !important;
  border-radius: 0.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: 1px solid var(--theme-border);
  margin-top: 0.5rem;
}}

.bg-secondary.text-white .display-4 {{
  font-weight: 700;
  letter-spacing: -0.03em;
}}

.bg-secondary.text-white .lead {{
  opacity: 0.85;
  font-size: 1.05rem;
}}

/* ------------------------------------------------------------------------------
 * Navigation & Search Bar (.navbar, .navbar-light, .bg-light)
 * ------------------------------------------------------------------------------ */
.navbar, .navbar-light.bg-light {{
  background-color: var(--bs-body-bg) !important;
  border-bottom: 1px solid var(--bs-border-color) !important;
  padding: 0.75rem 0 !important;
}}

/* ------------------------------------------------------------------------------
 * Form Search Input (.form-control)
 * ------------------------------------------------------------------------------ */
.form-control {{
  background-color: var(--bs-body-bg) !important;
  color: var(--bs-body-color) !important;
  border: 1px solid var(--bs-border-color) !important;
  border-radius: 0.5rem !important;
  padding: 0.6rem 1rem !important;
  font-size: 0.95rem !important;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}}

.form-control::placeholder {{
  color: var(--bs-body-color) !important;
  opacity: 0.5;
}}

.form-control:focus {{
  background-color: var(--bs-body-bg) !important;
  color: var(--bs-body-color) !important;
  border-color: var(--theme-primary) !important;
  box-shadow: 0 0 0 3px var(--bs-focus-ring-color) !important;
  outline: none !important;
}}

/* ------------------------------------------------------------------------------
 * Search Button (#search-button, .btn-outline-success.btn-light)
 * ------------------------------------------------------------------------------ */
#search-button,
.btn-outline-success.btn-light,
.btn-outline-success {{
  background-color: var(--theme-primary) !important;
  color: var(--theme-primary-fg) !important;
  border: 1px solid var(--theme-primary) !important;
  border-radius: 0.5rem !important;
  padding: 0.6rem 1.4rem !important;
  font-weight: 600 !important;
  font-size: 0.95rem !important;
  margin-left: 0.5rem !important;
  cursor: pointer;
  transition: filter 0.15s ease-in-out, transform 0.1s ease-in-out, opacity 0.15s ease-in-out;
}}

#search-button:hover,
.btn-outline-success.btn-light:hover,
.btn-outline-success:hover {{
  filter: brightness(0.92);
  transform: translateY(-1px);
}}

#search-button:active,
.btn-outline-success.btn-light:active,
.btn-outline-success:active {{
  transform: translateY(0);
}}

/* ------------------------------------------------------------------------------
 * Divider (hr)
 * ------------------------------------------------------------------------------ */
hr {{
  border-top: 1px solid var(--bs-border-color) !important;
  opacity: 1 !important;
  margin: 1.5rem 0 !important;
}}

/* ------------------------------------------------------------------------------
 * Results Table (.table, .table-info, .table-light)
 * ------------------------------------------------------------------------------ */
.table-responsive {{
  border: 1px solid var(--bs-border-color);
  border-radius: 0.5rem;
  overflow: hidden;
  background-color: var(--bs-body-bg);
}}

.table {{
  --bs-table-bg: var(--bs-body-bg);
  --bs-table-color: var(--bs-body-color);
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  margin-bottom: 0 !important;
}}

/* Table Header (.table-info) */
.table thead tr.table-info,
.table-info,
.table-info > th,
.table-info > td {{
  --bs-table-bg: var(--theme-muted) !important;
  --bs-table-color: var(--bs-body-color) !important;
  background-color: var(--theme-muted) !important;
  color: var(--bs-body-color) !important;
  border-bottom: 1px solid var(--bs-border-color) !important;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 0.75rem 1rem !important;
}}

/* Table Rows (.table-light) */
.table tbody tr.table-light,
.table-light,
.table-light > th,
.table-light > td {{
  --bs-table-bg: var(--bs-body-bg) !important;
  --bs-table-color: var(--bs-body-color) !important;
  background-color: var(--bs-body-bg) !important;
  color: var(--bs-body-color) !important;
  border-bottom: 1px solid var(--bs-border-color) !important;
  font-size: 0.9rem;
  padding: 0.75rem 1rem !important;
  transition: background-color 0.12s ease;
}}

.table tbody tr.table-light:hover,
.table tbody tr.table-light:hover > td {{
  background-color: var(--theme-hover) !important;
}}

.table tbody tr:last-child > td {{
  border-bottom: none !important;
}}
"""

def main():
    for name, cfg in THEMES.items():
        base = BASES[cfg["base"]]
        l = base["light"]
        d = base["dark"]
        css = TEMPLATE.format(
            title=name.capitalize(),
            light_pri=cfg["light_pri"],
            light_pri_rgb=cfg["light_pri_rgb"],
            light_pri_fg=cfg["light_pri_fg"],
            l_bg=l["bg"],
            l_bg_rgb=l["bg_rgb"],
            l_fg=l["fg"],
            l_fg_rgb=l["fg_rgb"],
            l_border=l["border"],
            l_muted=l["muted"],
            l_hover=l["hover"],
            l_header_bg=l["header_bg"],
            l_header_fg=l["header_fg"],
            dark_pri=cfg["dark_pri"],
            dark_pri_rgb=cfg["dark_pri_rgb"],
            dark_pri_fg=cfg["dark_pri_fg"],
            d_bg=d["bg"],
            d_bg_rgb=d["bg_rgb"],
            d_fg=d["fg"],
            d_fg_rgb=d["fg_rgb"],
            d_border=d["border"],
            d_muted=d["muted"],
            d_hover=d["hover"],
            d_header_bg=d["header_bg"],
            d_header_fg=d["header_fg"],
        )
        filepath = os.path.join(THEMES_DIR, f"{name}.css")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(css)
        print(f"Generated: {filepath}")

    print(f"Successfully generated {len(THEMES)} theme stylesheets!")

if __name__ == "__main__":
    main()
