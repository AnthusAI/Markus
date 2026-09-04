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
    And the site should include "assets/pipeline.svg"
    And "index.html" should contain "markus-pull-quote"
    And "index.html" should contain "markus-card-grid"
    And "index.html" should contain "markus-two-up"
    And "index.html" should contain "markus-figure"
    And "index.html" should contain "markus-details"
    And "index.html" should contain "markus-aside"
    And "index.html" should contain "markus-metric"
    And "gallery.html" should contain "markus-callout--note"
    And "gallery.html" should contain "markus-callout--warning"
    And "gallery.html" should contain "markus-callout--tip"
    And "gallery.html" should contain "markus-callout--caution"
    And "gfm.html" should contain "<table>"
    And "gfm.html" should contain "checkbox"
