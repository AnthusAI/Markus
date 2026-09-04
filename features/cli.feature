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
