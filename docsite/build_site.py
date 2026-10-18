import argparse
import shutil
import tempfile
from pathlib import Path

from papyrus_content.markus_renderer.build import build_markus_site
from papyrus_content.markus_renderer.shell import SiteChrome

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SITE_CONTENT_DIRECTORY = REPOSITORY_ROOT / "site"
SITE_THEME_NAME = "catppuccin"
SITE_STYLESHEET = REPOSITORY_ROOT / "src" / "markusmd" / "static" / "site.css"
def render_site_banner(page_context):
    navigation_links = "".join(
        f'<a href="{page_context.prefix}{item.href}"'
        + (' aria-current="page"' if item.href == page_context.active_href else "")
        + f">{item.label}</a>"
        for item in page_context.nav_items
    )
    return (
        '<header class="site-banner">'
        f'<a class="site-wordmark" href="{page_context.prefix}index.html">Markus</a>'
        '<p class="site-tagline">GitHub-flavored Markdown, plus a small vocabulary for layout intent.</p>'
        f'<div class="site-nav-container"><nav class="site-nav" aria-label="Demo">{navigation_links}</nav></div>'
        "</header>"
    )


SITE_CHROME = SiteChrome(
    site_name="Markus",
    head_html=f"<script>document.documentElement.setAttribute('data-theme','{SITE_THEME_NAME}')</script>",
    render_masthead=render_site_banner,
    footer_html='<p>Built with <a href="https://github.com/AnthusAI/Papyrus">Papyrus</a>. Source on <a href="https://github.com/AnthusAI/Markus">GitHub</a>.</p>',
)


def stage_papyrus_content_layout(staging_directory: Path) -> None:
    shutil.copytree(SITE_CONTENT_DIRECTORY / "assets", staging_directory / "assets")
    articles_directory = staging_directory / "articles"
    articles_directory.mkdir()
    for source_page in SITE_CONTENT_DIRECTORY.glob("*.md"):
        page_text = source_page.read_text(encoding="utf-8")
        if source_page.name == "index.md":
            for article_page in ("gallery", "gfm"):
                page_text = page_text.replace(f"({article_page}.html)", f"(articles/{article_page}.html)")
            (staging_directory / "index.md").write_text(page_text, encoding="utf-8")
        else:
            (articles_directory / source_page.name).write_text(page_text, encoding="utf-8")


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
    with tempfile.TemporaryDirectory(prefix="markus-site-content-") as staging_name:
        staging_directory = Path(staging_name)
        stage_papyrus_content_layout(staging_directory)
        build_result = build_markus_site(
            content_dir=staging_directory,
            out_dir=output_directory,
            theme=SITE_THEME_NAME,
            site_css=SITE_STYLESHEET,
            chrome=SITE_CHROME,
        )
    write_redirects_from_former_urls(output_directory)
    return build_result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the Markus documentation site with Papyrus.")
    parser.add_argument("--out", type=Path, default=REPOSITORY_ROOT / "_site")
    arguments = parser.parse_args()
    result = build_documentation_site(arguments.out)
    print(f"Built {len(result.pages)} pages into {result.out_dir}")
