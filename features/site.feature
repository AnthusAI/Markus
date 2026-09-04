Feature: GitHub Pages demo site
  As a visitor evaluating Markus
  I want a static demo that exercises every built-in directive
  So that I can see the language without installing anything

  Scenario: The bundled site sources cover the full vocabulary
    Given the bundled Markus site sources
    When I build the demo site
    Then the site should include "index.html"
    And the site should include "gallery.html"
    And the site should include "gfm.html"
    And the site should include "markus.css"
    And the site should include "themes/hackerman.css"
    And the site should include "themes/ristretto.css"
    And the site should include "themes/gruvbox.css"
    And the site should include "themes/lumon.css"
    And the site should include "themes/tokyo-night.css"
    And the site should include "themes/catppuccin-latte.css"
    And the site should include "themes/flexoki-light.css"
    And the site should include "themes/white.css"
    And the site should include "themes/osaka-jade.css"
    And the site should include "themes/catppuccin.css"
    And the site should include "themes/ethereal.css"
    And the site should include "themes/everforest.css"
    And the site should include "themes/kanagawa.css"
    And the site should include "themes/last-horizon.css"
    And the site should include "themes/lupine.css"
    And the site should include "themes/matte-black.css"
    And the site should include "themes/miasma.css"
    And the site should include "themes/nord.css"
    And the site should include "themes/retro-82.css"
    And the site should include "themes/rose-pine.css"
    And the site should include "themes/solitude.css"
    And the site should include "themes/vantablack.css"
    And the site should include "assets/pipeline.svg"
    And "index.html" should contain "markus-pull-quote"
    And "index.html" should contain "markus-card-grid"
    And "index.html" should contain "markus-two-up"
    And "index.html" should contain "markus-figure"
    And "index.html" should contain "markus-details"
    And "index.html" should contain "markus-aside"
    And "index.html" should contain "markus-metric"
    And "index.html" should contain "markus-tabs"
    And "index.html" should contain "markus-step-list"
    And "index.html" should contain "markus-video"
    And "index.html" should contain "markus-timeline"
    And "index.html" should contain "markus-timeline-event"
    And "gallery.html" should contain "markus-callout--note"
    And "gallery.html" should contain "markus-callout--warning"
    And "gallery.html" should contain "markus-callout--tip"
    And "gallery.html" should contain "markus-callout--caution"
    And "gfm.html" should contain "<table>"
    And "gfm.html" should contain "checkbox"
    And "index.html" should contain "copy-button"
    And "gallery.html" should contain "copy-button"
    And "gfm.html" should contain "copy-button"

  Scenario: Code blocks include accessible copy-to-clipboard buttons
    Given the bundled Markus site sources
    When I build the demo site
    Then "index.html" should contain "code-block-wrapper"
    And "index.html" should contain "copy-button"
    And "index.html" should contain "Copy code to clipboard"
    And "gallery.html" should contain "code-block-wrapper"
    And "gallery.html" should contain "copy-button"
    And "gfm.html" should contain "code-block-wrapper"
    And "gfm.html" should contain "copy-button"
    And "site.css" should contain ".copy-button"

  Scenario: The demo site defaults to the catppuccin theme
    Given the bundled Markus site sources
    When I build the demo site
    Then "index.html" should contain "themes/catppuccin.css"
    And "index.html" should contain "catppuccin"
    And "gallery.html" should contain "themes/catppuccin.css"
    And "gallery.html" should contain "catppuccin"
    And "gfm.html" should contain "themes/catppuccin.css"
    And "gfm.html" should contain "catppuccin"


