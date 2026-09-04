Feature: Markus command line
  As a writer in a terminal
  I want to convert, validate, and inspect Markus files
  So that I can publish HTML without embedding the library myself

  Scenario: Convert a file to HTML
    Given a Markus file "page.md" with:
      """
      # Hello Markus
      """
    When I run "markus convert page.md --fragment --no-css"
    Then the command should succeed
    And stdout should contain "<h1>Hello Markus</h1>"

  Scenario: Validate a well-formed file
    Given a Markus file "ok.md" with:
      """
      :::tip
      Ship the small vocabulary first.
      :::
      """
    When I run "markus validate ok.md"
    Then the command should succeed
    And stdout should contain "ok"

  Scenario: Validate rejects unknown directives
    Given a Markus file "bad.md" with:
      """
      :::carousel
      Nope.
      :::
      """
    When I run "markus validate bad.md"
    Then the command should fail
    And stderr should contain "Unknown directive 'carousel'"

  Scenario: Print a JSON AST
    Given a Markus file "quote.md" with:
      """
      :::pull-quote{attribution="Ada"}
      Make it matter.
      :::
      """
    When I run "markus ast quote.md"
    Then the command should succeed
    And stdout should contain "pull-quote"
    And stdout should contain "Ada"

  Scenario: Convert a file to HTML with minified CSS
    Given a Markus file "styled.md" with:
      """
      # Styled Page
      """
    When I run "markus convert styled.md --minify-css"
    Then the command should succeed
    And stdout should contain "<h1>Styled Page</h1>"
    And stdout should contain "<style>"
    And stdout should not contain "/* Markus default presentation layer"
    And stdout should contain ":root{"

  Scenario: Convert with minified CSS and no-css omits CSS
    Given a Markus file "plain.md" with:
      """
      # Plain Page
      """
    When I run "markus convert plain.md --minify-css --no-css"
    Then the command should succeed
    And stdout should contain "<h1>Plain Page</h1>"
    And stdout should not contain "<style>"

  Scenario: Convert fragment with minified CSS
    Given a Markus file "frag.md" with:
      """
      # Fragment
      """
    When I run "markus convert frag.md --fragment --minify-css"
    Then the command should succeed
    And stdout should contain "<style>"
    And stdout should not contain "/* Markus default presentation layer"
    And stdout should contain "markus-document"
    And stdout should contain "<h1>Fragment</h1>"
