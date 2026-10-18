Feature: Heading anchors
  As an author linking to sections of a document
  I want every heading to have a stable id and to be able to choose one
  So that tables of contents and cross references need no raw anchor tags

  Scenario: Headings get a generated slug id
    Given the Markus source:
      """
      ## Example 1: Use AI models from any company's AI API
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain the markup:
      """
      <h2 id="example-1-use-ai-models-from-any-companys-ai-api">
      """

  Scenario: A custom id suffix sets the heading id and is not shown
    Given the Markus source:
      """
      ## Use AI models from any company's API {#ai-api-multiplexer}
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain the markup:
      """
      <h2 id="ai-api-multiplexer">Use AI models from any company's API</h2>
      """
    And the HTML should not contain "{#"

  Scenario: Links to a heading id resolve in the same document
    Given the Markus source:
      """
      See [the multiplexer](#ai-api-multiplexer) and [the basics](#the-basics).

      ## The basics

      ## Multiplexing {#ai-api-multiplexer}
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain the markup:
      """
      <a href="#ai-api-multiplexer">the multiplexer</a>
      """
    And the HTML should contain the markup:
      """
      <h2 id="the-basics">The basics</h2>
      """
    And the HTML should contain the markup:
      """
      <h2 id="ai-api-multiplexer">Multiplexing</h2>
      """

  Scenario: Slugs ignore inline markup and punctuation
    Given the Markus source:
      """
      ### The `--flag` option & **bold** [link](https://example.com)!
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain the markup:
      """
      <h3 id="the-flag-option-bold-link">
      """

  Scenario: Repeated headings get numbered suffixes across the whole document
    Given the Markus source:
      """
      ## Notes

      Text.

      :::callout
      Between.
      :::

      ## Notes

      ## Notes
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain the markup:
      """
      <h2 id="notes">Notes</h2>
      """
    And the HTML should contain the markup:
      """
      <h2 id="notes-1">Notes</h2>
      """
    And the HTML should contain the markup:
      """
      <h2 id="notes-2">Notes</h2>
      """

  Scenario: Generated ids are stable when a heading is converted to a custom id
    Given the Markus source:
      """
      ## Setup {#install}

      ## Install
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain the markup:
      """
      <h2 id="install">Setup</h2>
      """
    And the HTML should contain the markup:
      """
      <h2 id="install-1">Install</h2>
      """

  Scenario: An explicit id later in the document wins over an earlier generated slug
    Given the Markus source:
      """
      ### [Safeguard Retry Loops](#safeguard-retry-loops)

      ## Example 3: Add a safeguard retry loop {#safeguard-retry-loops}
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain the markup:
      """
      <h2 id="safeguard-retry-loops">Example 3: Add a safeguard retry loop</h2>
      """
    And the HTML should contain the markup:
      """
      <h3 id="safeguard-retry-loops-1">
      """

  Scenario: Non-English headings keep their letters
    Given the Markus source:
      """
      ## Sagrada Família y más
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain the markup:
      """
      <h2 id="sagrada-família-y-más">
      """

  Scenario: Headings inside directives are anchored too
    Given the Markus source:
      """
      :::details{summary="More"}
      ### Inside {#inner}
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain the markup:
      """
      <h3 id="inner">Inside</h3>
      """

  Scenario: A duplicate custom id is rejected
    Given the Markus source:
      """
      ## One {#same}

      ## Two {#same}
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "Duplicate heading id 'same'"
    And the error should mention line 3

  Scenario: A malformed custom id is rejected
    Given the Markus source:
      """
      ## Title {#1 bad}
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "Invalid heading id"
    And the error should mention line 1

  Scenario: Braces that are not an id suffix stay literal
    Given the Markus source:
      """
      ## Set {a, b} notation
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain "Set {a, b} notation"
