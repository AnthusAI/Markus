import argparse
import html
import json
import shutil
import tempfile
from pathlib import Path

from papyrus_content.markus_renderer.build import build_markus_site
from papyrus_content.markus_renderer.docs_site import (
    DocsSiteConfig,
    stage_generated_pages,
    write_sitemap_and_not_found_page,
)
from papyrus_content.markus_renderer.shell import SiteChrome

from markusmd.themes import THEME_MODES

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SITE_CONTENT_DIRECTORY = REPOSITORY_ROOT / "site"
SITE_CUSTOM_DOMAIN = "markus.anth.us"
SITE_STYLESHEET = SITE_CONTENT_DIRECTORY / "site.css"
SITE_URL = "https://markus.anth.us/"
# Papyrus writes sitemap.xml and 404.html for a docs site that declares its public address.
SITEMAP_CONFIG = DocsSiteConfig(
    site_name="Markus",
    tagline="",
    documentation_directory=SITE_CONTENT_DIRECTORY,
    source_repository_url="https://github.com/AnthusAI/Markus",
    published_site_url=SITE_URL,
)
HOME_HREF = "index.html"

# The sidebar, in reading order. Every page under site/ must appear here exactly
# once, so a new feature page cannot ship without a place in the docs.
NAVIGATION = (
    (
        "Start",
        (
            (HOME_HREF, "Overview"),
            ("articles/getting-started.html", "Get started"),
            ("articles/features.html", "Feature index"),
        ),
    ),
    (
        "Language",
        (
            ("articles/demo-syntax.html", "Syntax and metadata"),
            ("articles/gfm-features.html", "GitHub Flavored Markdown"),
            ("articles/demo-highlight.html", "Highlight"),
            ("articles/demo-heading-anchors.html", "Heading anchors"),
            ("articles/demo-tables.html", "Tables"),
        ),
    ),
    (
        "Text blocks",
        (
            ("articles/demo-callouts.html", "Callouts and asides"),
            ("articles/demo-pull-quote.html", "Pull quote"),
            ("articles/demo-details.html", "Details"),
            ("articles/demo-editorial-finding.html", "Editorial finding"),
            ("articles/demo-example.html", "Example"),
        ),
    ),
    (
        "Layout",
        (
            ("articles/demo-cards.html", "Card grid and cards"),
            ("articles/demo-two-up.html", "Two-up and columns"),
            ("articles/demo-tabs.html", "Tabs"),
        ),
    ),
    (
        "Media and data",
        (
            ("articles/demo-media.html", "Figure and video"),
            ("articles/demo-metric.html", "Metric"),
            ("articles/demo-bar-chart.html", "Bar chart"),
        ),
    ),
    (
        "Sequences and flows",
        (
            ("articles/demo-steps.html", "Step list"),
            ("articles/demo-timeline.html", "Timeline"),
            ("articles/demo-conversation.html", "Conversation"),
            ("articles/demo-diagram.html", "Diagram"),
        ),
    ),
    (
        "Showcase",
        (
            ("articles/gallery.html", "Gallery"),
            ("articles/gfm.html", "Markus and GFM"),
        ),
    ),
)

# A volt square edged in ink, the wordmark's mark, inline so it resolves at every page depth.
FAVICON = (
    '<link rel="icon" href="data:image/svg+xml,'
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E"
    "%3Crect x='1' y='1' width='14' height='14' fill='%23c6f135'"
    " stroke='%230f1011' stroke-width='2'/%3E"
    '%3C/svg%3E">'
)

# Every bundled Markus theme, offered in the theme picker in registry order:
# light-and-dark families first (Solarized leading), then single-mode themes.
# "Markus" is the design-system default and also follows light or dark.
SITE_THEMES = list(THEME_MODES)
MODE_MARKS = {"both": "\u25d0", "light": "\u25cb", "dark": "\u25cf"}
MODE_GROUPS = (
    ("both", "Light and dark"),
    ("light", "Light only"),
    ("dark", "Dark only"),
)
THEME_NAMES = {"github": "GitHub", "one": "One", "rose-pine": "Rosé Pine", "retro-82": "Retro 82"}

# Link previews: every page shares the 1200x630 card rendered from
# docsite/social-preview.html. Crawlers need an absolute image URL.
SOCIAL_DESCRIPTION = (
    "GitHub-flavored Markdown with a small vocabulary of semantic layout directives."
)
SOCIAL_META = (
    '<meta name="description" content="' + SOCIAL_DESCRIPTION + '">'
    '<meta property="og:type" content="website">'
    '<meta property="og:site_name" content="Markus">'
    '<meta property="og:title" content="Markus: Markdown for layout intent">'
    '<meta property="og:description" content="' + SOCIAL_DESCRIPTION + '">'
    f'<meta property="og:image" content="{SITE_URL}assets/social-preview.png">'
    '<meta property="og:image:width" content="1200">'
    '<meta property="og:image:height" content="630">'
    '<meta property="og:image:alt" content="Markus: Markdown for layout intent. '
    'A Markus tip directive beside its rendered preview.">'
    '<meta name="twitter:card" content="summary_large_image">'
    f'<meta name="twitter:image" content="{SITE_URL}assets/social-preview.png">'
)

# Applied before first paint so a reader's saved choices never flash the defaults.
# A single-mode theme marks the root so the light/dark switch can hide.
COLOR_SCHEME_BOOTSTRAP = (
    "<script>try{var r=document.documentElement,"
    "s=localStorage.getItem('markus-color-scheme'),t=localStorage.getItem('markus-theme'),"
    f"m={json.dumps(THEME_MODES)};"
    "if(s==='light'||s==='dark')r.setAttribute('data-color-scheme',s);"
    "if(m[t]){r.setAttribute('data-theme',t);r.setAttribute('data-theme-mode',m[t])}"
    "}catch(e){}</script>"
)


def theme_label(theme: str) -> str:
    return THEME_NAMES.get(theme) or " ".join(word.capitalize() for word in theme.split("-"))


def theme_option(value: str, label: str, mode: str) -> str:
    return (
        f'<option value="{html.escape(value)}" data-mode="{mode}">'
        f"{MODE_MARKS[mode]} {html.escape(label)}</option>"
    )


def render_theme_picker() -> str:
    groups = []
    for mode, group_label in MODE_GROUPS:
        options = [theme_option("", "Markus", "both")] if mode == "both" else []
        options += [
            theme_option(theme, theme_label(theme), mode)
            for theme in SITE_THEMES
            if THEME_MODES[theme] == mode
        ]
        groups.append(
            f'<optgroup label="{MODE_MARKS[mode]} {group_label}">{"".join(options)}</optgroup>'
        )
    return (
        '<label class="site-theme">'
        '<span class="site-theme-label">Theme</span>'
        f'<select data-theme-picker aria-label="Markus theme">{"".join(groups)}</select>'
        "</label>"
    )


def render_navigation(page_context) -> str:
    groups = []
    for group_label, entries in NAVIGATION:
        items = []
        for href, label in entries:
            current = ' aria-current="page"' if href == page_context.active_href else ""
            home = " data-home" if href == HOME_HREF else ""
            link = f'<a href="{page_context.prefix}{href}"{current}{home}>{html.escape(label)}</a>'
            items.append(f"<li>{link}</li>")
        groups.append(
            '<div class="site-nav-group">'
            f'<p class="site-nav-label">{html.escape(group_label)}</p>'
            f'<ul class="site-nav-list">{"".join(items)}</ul>'
            "</div>"
        )
    return "".join(groups)


def render_site_banner(page_context) -> str:
    return (
        '<header class="site-banner">'
        '<div class="site-topbar">'
        f'<a class="site-wordmark" href="{page_context.prefix}{HOME_HREF}">'
        '<span class="site-wordmark-mark" aria-hidden="true"></span>Markus</a>'
        '<nav class="site-links" aria-label="Project">'
        '<a href="https://github.com/AnthusAI/Markus">GitHub</a>'
        '<a href="https://pypi.org/project/anthus-markus/">PyPI</a>'
        "</nav>"
        f"{render_theme_picker()}"
        '<div class="site-scheme" role="group" aria-label="Color scheme">'
        '<button type="button" data-scheme="system" aria-pressed="true">Auto</button>'
        '<button type="button" data-scheme="light" aria-pressed="false">Light</button>'
        '<button type="button" data-scheme="dark" aria-pressed="false">Dark</button>'
        "</div>"
        "</div>"
        '<details class="site-menu">'
        "<summary>Contents</summary>"
        '<nav class="site-sidebar" aria-label="Documentation">'
        f"{render_navigation(page_context)}</nav>"
        "</details>"
        "</header>"
    )


# The standard Anthus platform footer: the markup and links of the shared
# AnthusAI/anthus-footer React component and its canonical site registry,
# rendered statically here and styled from the site's theme tokens.
ANTHUS_COMMUNITY_LINKS = (
    (
        "Contact us",
        "https://docs.google.com/forms/d/e/1FAIpQLSdWlt4KpwPSBHzg3o8fikHcfrzxo5rCcV-0-zDt815NZ1tcyg"
        "/viewform?usp=sf_link",
    ),
    ("GitHub", "https://github.com/AnthusAI"),
    ("LinkedIn", "https://www.linkedin.com/in/ryanalynporter/"),
    ("Discord", "https://discord.gg/uStyWraJ2M"),
)
ANTHUS_COLUMNS = (
    (
        "Anthus",
        (
            ("Anth.us", "https://anth.us/", False),
            ("AI Solutions", "https://anth.us/ai-solutions", False),
            ("Anthus Platform", "https://anth.us/platform", False),
            ("Articles", "https://anth.us/blog", False),
        ),
    ),
    (
        "Anthus Platform",
        (
            ("Primus", "https://primus.anth.us/", False),
            ("Tactus", "https://tactus.anth.us/", False),
            ("Korporus", "https://korpor.us/", False),
            ("Biblicus", "https://anthusai.github.io/Biblicus/", False),
            ("Babulus", "https://babul.us/", False),
            ("Kanbus", "https://kanb.us/", False),
            ("Caducus", "https://caduc.us/", False),
        ),
    ),
    (
        "Markus",
        (
            ("Documentation", "https://markus.anth.us/", False),
            ("GitHub", "https://github.com/AnthusAI/Markus", True),
            ("PyPI", "https://pypi.org/project/anthus-markus/", True),
            ("Built with Papyrus", "https://github.com/AnthusAI/Papyrus", True),
        ),
    ),
)


def anthus_link(label: str, href: str, external: bool) -> str:
    target = ' target="_blank" rel="noreferrer"' if external else ""
    return f'<a href="{html.escape(href)}"{target}>{html.escape(label)}</a>'


def render_anthus_footer() -> str:
    community = '<span aria-hidden="true">·</span>'.join(
        anthus_link(label, href, True) for label, href in ANTHUS_COMMUNITY_LINKS
    )
    columns = "".join(
        '<div class="anthus-footer-panel">'
        f"<h3>{html.escape(title)}</h3>"
        '<ul class="anthus-footer-list">'
        + "".join(f"<li>{anthus_link(*link)}</li>" for link in links)
        + "</ul></div>"
        for title, links in ANTHUS_COLUMNS
    )
    return (
        '<div class="anthus-footer">'
        f'<div class="anthus-footer-community">{community}</div>'
        '<div class="anthus-footer-grid">'
        '<div class="anthus-footer-panel anthus-footer-panel--accent">'
        '<span class="anthus-footer-eyebrow">Part of the Anthus Platform</span>'
        "<h2>Markus</h2>"
        "<p>Markus is GitHub-flavored Markdown with a small vocabulary for layout intent. "
        "Authors encode meaning; the renderer turns it into accessible HTML.</p>"
        "</div>"
        f"{columns}"
        "</div>"
        '<div class="anthus-footer-bottom">'
        "<span>Built by Anthus AI Solutions</span>"
        "<span>Free and open-source Anthus platform components where applicable</span>"
        "</div>"
        "</div>"
    )


SITE_CHROME = SiteChrome(
    site_name="Markus",
    head_html=FAVICON + SOCIAL_META + COLOR_SCHEME_BOOTSTRAP,
    render_masthead=render_site_banner,
    footer_html=render_anthus_footer(),
    scripts=("assets/site.js",),
)


def navigation_pages() -> list[str]:
    return [href for _, entries in NAVIGATION for href, _ in entries]


def assert_navigation_covers_site() -> None:
    listed = navigation_pages()
    duplicates = sorted({href for href in listed if listed.count(href) > 1})
    if duplicates:
        raise SystemExit(f"Pages listed twice in NAVIGATION: {', '.join(duplicates)}")
    on_disk = {
        HOME_HREF if page.name == "index.md" else f"articles/{page.stem}.html"
        for page in SITE_CONTENT_DIRECTORY.glob("*.md")
    }
    missing = sorted(on_disk - set(listed))
    stale = sorted(set(listed) - on_disk)
    if missing or stale:
        raise SystemExit(
            "NAVIGATION and site/ disagree."
            + (f" Not in NAVIGATION: {', '.join(missing)}." if missing else "")
            + (f" No page for: {', '.join(stale)}." if stale else "")
        )


def stage_papyrus_content_layout(staging_directory: Path) -> None:
    shutil.copytree(SITE_CONTENT_DIRECTORY / "assets", staging_directory / "assets")
    articles_directory = staging_directory / "articles"
    articles_directory.mkdir()
    for source_page in SITE_CONTENT_DIRECTORY.glob("*.md"):
        page_text = source_page.read_text(encoding="utf-8")
        if source_page.name == "index.md":
            for article_page in SITE_CONTENT_DIRECTORY.glob("*.md"):
                if article_page.name != "index.md":
                    page_text = page_text.replace(
                        f"]({article_page.stem}.html", f"](articles/{article_page.stem}.html"
                    )
            (staging_directory / "index.md").write_text(page_text, encoding="utf-8")
        else:
            page_text = page_text.replace("](index.html", "](../index.html")
            page_text = page_text.replace('src="assets/', 'src="../assets/')
            page_text = page_text.replace("](assets/", "](../assets/")
            (articles_directory / source_page.name).write_text(page_text, encoding="utf-8")


def write_robots(output_directory: Path) -> None:
    (output_directory / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8"
    )


def write_custom_domain(output_directory: Path) -> None:
    (output_directory / "CNAME").write_text(f"{SITE_CUSTOM_DOMAIN}\n", encoding="utf-8")


def write_redirects_from_former_urls(output_directory: Path) -> None:
    for former_page in ("gallery", "gfm"):
        (output_directory / f"{former_page}.html").write_text(
            '<!DOCTYPE html><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url=articles/{former_page}.html">'
            f'<link rel="canonical" href="articles/{former_page}.html">'
            f'<a href="articles/{former_page}.html">Moved to articles/{former_page}.html</a>',
            encoding="utf-8",
        )


def build_documentation_site(output_directory: Path):
    assert_navigation_covers_site()
    with tempfile.TemporaryDirectory(prefix="markus-site-content-") as staging_name:
        staging_directory = Path(staging_name)
        stage_papyrus_content_layout(staging_directory)
        stage_generated_pages(staging_directory)
        build_result = build_markus_site(
            content_dir=staging_directory,
            out_dir=output_directory,
            theme=None,
            site_css=SITE_STYLESHEET,
            chrome=SITE_CHROME,
        )
        write_redirects_from_former_urls(output_directory)
        # content_directory also writes the .md twins, llms.txt and llms-full.txt
        write_sitemap_and_not_found_page(SITEMAP_CONFIG, output_directory, content_directory=staging_directory)
    write_robots(output_directory)
    write_custom_domain(output_directory)
    return build_result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build the Markus documentation site with Papyrus."
    )
    parser.add_argument("--out", type=Path, default=REPOSITORY_ROOT / "_site")
    arguments = parser.parse_args()
    result = build_documentation_site(arguments.out)
    print(f"Built {len(result.pages)} pages into {result.out_dir}")
