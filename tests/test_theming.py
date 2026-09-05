"""
Automated unit & integration tests for hiSHtory Web UI theming.
Validates CSS variables, light/dark mode support, container startup logic,
conflict resolution, and Nginx injection configuration.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
THEMES_DIR = os.path.join(REPO_ROOT, "root", "usr", "share", "hishtory", "themes")

EXPECTED_THEMES = [
    "lime", "amber", "blue", "cyan", "emerald", "fuchsia", "green", "indigo",
    "orange", "pink", "purple", "red", "rose", "sky", "teal", "violet",
    "yellow", "zinc", "slate", "stone", "gray", "neutral"
]

REQUIRED_CSS_TOKENS = [
    ":root",
    "color-scheme: light",
    "--theme-primary",
    "--theme-primary-rgb",
    "--theme-bg",
    "--theme-fg",
    "--theme-border",
    "--bs-primary",
    "--bs-primary-rgb",
    "--bs-body-bg",
    "--bs-body-color",
    "--bs-border-color",
    "@media (prefers-color-scheme: dark)",
    "color-scheme: dark",
    ".bg-secondary.text-white",
    ".navbar",
    ".form-control",
    "#search-button",
    ".table",
    ".table-info",
    ".table-light"
]


class TestTheming(unittest.TestCase):

    def test_all_theme_files_exist(self):
        """Verify that all expected 22 theme files exist in root/usr/share/hishtory/themes."""
        self.assertTrue(os.path.isdir(THEMES_DIR), f"Themes directory does not exist: {THEMES_DIR}")
        files = os.listdir(THEMES_DIR)
        for theme in EXPECTED_THEMES:
            filename = f"{theme}.css"
            self.assertIn(filename, files, f"Missing theme file: {filename}")

    def test_theme_css_content(self):
        """Verify each theme file contains required CSS variables and light/dark mode media queries."""
        for theme in EXPECTED_THEMES:
            filepath = os.path.join(THEMES_DIR, f"{theme}.css")
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            for token in REQUIRED_CSS_TOKENS:
                self.assertIn(token, content, f"Theme '{theme}' missing required token: {token}")

    def test_nginx_conf_syntax(self):
        """Verify that nginx.conf has proper include directives and location blocks."""
        nginx_conf = os.path.join(REPO_ROOT, "root", "etc", "nginx", "nginx.conf")
        with open(nginx_conf, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("location = / {", content, "Missing exact root location in nginx.conf")
        self.assertIn("add_after_body /_theme_tag;", content, "Missing add_after_body directive in root location")
        self.assertIn("include /etc/nginx/conf.d/*.conf;", content, "Missing wildcard conf.d include")
        self.assertIn('proxy_set_header Accept-Encoding "";', content, "Accept-Encoding must be cleared for addition filter")

    def test_theme_startup_logic_builtin(self):
        """Simulate container init script pointing dynamically to a built-in theme in conf.d/theme.conf."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = os.path.join(tmpdir, "config")
            conf_d_dir = os.path.join(tmpdir, "etc", "nginx", "conf.d")
            os.makedirs(config_dir)
            os.makedirs(conf_d_dir)

            test_script = f"""
            set -e
            THEME="lime"
            CONVENTIONAL_THEME="{config_dir}/theme.css"
            BUILTIN_THEMES_DIR="{THEMES_DIR}"
            THEME_CONF="{conf_d_dir}/theme.conf"

            ACTIVE_THEME_FILE=""

            if [ -f "$CONVENTIONAL_THEME" ]; then
                ACTIVE_THEME_FILE="$CONVENTIONAL_THEME"
            elif [ -n "$THEME" ]; then
                BUILTIN_SOURCE="${{BUILTIN_THEMES_DIR}}/${{THEME}}.css"
                if [ -f "$BUILTIN_SOURCE" ]; then
                    ACTIVE_THEME_FILE="$BUILTIN_SOURCE"
                fi
            fi

            if [ -n "$ACTIVE_THEME_FILE" ]; then
                cat <<EOF > "$THEME_CONF"
location = /theme.css {{
    alias ${{ACTIVE_THEME_FILE}};
    default_type text/css;
}}
location = /_theme_tag {{
    internal;
    default_type text/html;
    return 200 '<link rel="stylesheet" type="text/css" href="/theme.css">\\n';
}}
EOF
            else
                cat <<'EOF' > "$THEME_CONF"
location = /_theme_tag {{
    internal;
    return 204;
}}
EOF
            fi
            """

            res = subprocess.run(["bash", "-c", test_script], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, res.stderr)

            # /config volume should NOT have any file created or modified
            self.assertFalse(os.path.exists(os.path.join(config_dir, "theme.css")))

            with open(os.path.join(conf_d_dir, "theme.conf"), "r") as f:
                theme_conf = f.read()
            self.assertIn(f"alias {THEMES_DIR}/lime.css;", theme_conf)
            self.assertIn("location = /_theme_tag", theme_conf)
            self.assertIn("return 200", theme_conf)

    def test_theme_startup_logic_custom_theme_priority(self):
        """Verify that when /config/theme.css exists, it takes priority and points directly to /config/theme.css."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = os.path.join(tmpdir, "config")
            conf_d_dir = os.path.join(tmpdir, "etc", "nginx", "conf.d")
            os.makedirs(config_dir)
            os.makedirs(conf_d_dir)

            custom_css = os.path.join(config_dir, "theme.css")
            with open(custom_css, "w") as f:
                f.write("/* Custom User Theme */")

            test_script = f"""
            set -e
            THEME="lime"
            CONVENTIONAL_THEME="{config_dir}/theme.css"
            BUILTIN_THEMES_DIR="{THEMES_DIR}"
            THEME_CONF="{conf_d_dir}/theme.conf"

            ACTIVE_THEME_FILE=""

            if [ -f "$CONVENTIONAL_THEME" ]; then
                ACTIVE_THEME_FILE="$CONVENTIONAL_THEME"
            elif [ -n "$THEME" ]; then
                BUILTIN_SOURCE="${{BUILTIN_THEMES_DIR}}/${{THEME}}.css"
                if [ -f "$BUILTIN_SOURCE" ]; then
                    ACTIVE_THEME_FILE="$BUILTIN_SOURCE"
                fi
            fi

            if [ -n "$ACTIVE_THEME_FILE" ]; then
                cat <<EOF > "$THEME_CONF"
location = /theme.css {{
    alias ${{ACTIVE_THEME_FILE}};
    default_type text/css;
}}
location = /_theme_tag {{
    internal;
    default_type text/html;
    return 200 '<link rel="stylesheet" type="text/css" href="/theme.css">\\n';
}}
EOF
            fi
            """

            res = subprocess.run(["bash", "-c", test_script], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)

            with open(custom_css, "r") as f:
                content = f.read()
            self.assertEqual(content, "/* Custom User Theme */", "Custom user theme was unexpectedly modified!")

            with open(os.path.join(conf_d_dir, "theme.conf"), "r") as f:
                theme_conf = f.read()
            self.assertIn(f"alias {custom_css};", theme_conf)

    def test_theme_startup_logic_no_theme(self):
        """Verify that when no theme is set and no file exists, injection is disabled via return 204."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = os.path.join(tmpdir, "config")
            conf_d_dir = os.path.join(tmpdir, "etc", "nginx", "conf.d")
            os.makedirs(config_dir)
            os.makedirs(conf_d_dir)

            test_script = f"""
            set -e
            THEME=""
            CONVENTIONAL_THEME="{config_dir}/theme.css"
            BUILTIN_THEMES_DIR="{THEMES_DIR}"
            THEME_CONF="{conf_d_dir}/theme.conf"

            ACTIVE_THEME_FILE=""

            if [ -f "$CONVENTIONAL_THEME" ]; then
                ACTIVE_THEME_FILE="$CONVENTIONAL_THEME"
            elif [ -n "$THEME" ]; then
                BUILTIN_SOURCE="${{BUILTIN_THEMES_DIR}}/${{THEME}}.css"
                if [ -f "$BUILTIN_SOURCE" ]; then
                    ACTIVE_THEME_FILE="$BUILTIN_SOURCE"
                fi
            fi

            if [ -n "$ACTIVE_THEME_FILE" ]; then
                cat <<EOF > "$THEME_CONF"
location = /theme.css {{
    alias ${{ACTIVE_THEME_FILE}};
}}
EOF
            else
                cat <<'EOF' > "$THEME_CONF"
location = /_theme_tag {{
    internal;
    return 204;
}}
EOF
            fi
            """

            res = subprocess.run(["bash", "-c", test_script], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)

            with open(os.path.join(conf_d_dir, "theme.conf"), "r") as f:
                theme_conf = f.read()
            self.assertIn("return 204;", theme_conf)
            self.assertNotIn("alias", theme_conf)

    def test_s6_v3_structure(self):
        """Verify that s6-overlay v3 native services and dependency tree are properly configured."""
        s6_rc_dir = os.path.join(REPO_ROOT, "root", "etc", "s6-overlay", "s6-rc.d")
        cont_init_dir = os.path.join(REPO_ROOT, "root", "etc", "cont-init.d")

        # Ensure legacy cont-init.d is removed
        self.assertFalse(os.path.exists(cont_init_dir), "Legacy /etc/cont-init.d should not exist")

        # Verify svc-init oneshot service
        svc_init_dir = os.path.join(s6_rc_dir, "svc-init")
        self.assertTrue(os.path.isdir(svc_init_dir), "svc-init directory missing")
        with open(os.path.join(svc_init_dir, "type"), "r") as f:
            self.assertEqual(f.read().strip(), "oneshot")
        up_script = os.path.join(svc_init_dir, "up")
        self.assertTrue(os.path.isfile(up_script), "svc-init/up script missing")
        self.assertTrue(os.access(up_script, os.X_OK), "svc-init/up must be executable")

        # Verify user bundle registration
        user_content = os.path.join(s6_rc_dir, "user", "contents.d", "svc-init")
        self.assertTrue(os.path.isfile(user_content), "svc-init not registered in user/contents.d")

        # Verify dependent services declare dependency on svc-init
        for svc in ["svc-nginx", "svc-ingress", "svc-web"]:
            dep_file = os.path.join(s6_rc_dir, svc, "dependencies")
            dep_d_file = os.path.join(s6_rc_dir, svc, "dependencies.d", "svc-init")
            self.assertTrue(os.path.isfile(dep_file), f"{svc}/dependencies missing")
            with open(dep_file, "r") as f:
                self.assertIn("svc-init", f.read())
            self.assertTrue(os.path.isfile(dep_d_file), f"{svc}/dependencies.d/svc-init missing")


if __name__ == "__main__":
    unittest.main()
