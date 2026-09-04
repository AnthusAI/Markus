Feature: Directive validation
  As a maintainer of a content corpus
  I want unknown names and attributes to fail loudly
  So that Markus cannot quietly become an untyped CSS API

  Scenario: Unknown directives are rejected
    Given the Markus source:
      """
      :::grid{columns=3}
      Nope.
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "Unknown directive 'grid'"
    And the error should mention line 1

  Scenario: Unknown attributes are rejected
    Given the Markus source:
      """
      :::callout{kind="note" margin="2rem"}
      Nope.
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "Unknown attribute"
    And the error should contain "margin"

  Scenario: Two-up cannot contain a single column
    Given the Markus source:
      """
      :::two-up
      :::column
      Only one side.
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "exactly two column children"

  Scenario: Card grids cannot contain free Markdown
    Given the Markus source:
      """
      :::card-grid
      A stray paragraph.

      :::card
      ## Card
      Body.
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "may only contain card blocks"

  Scenario: Unclosed directives are a syntax error
    Given the Markus source:
      """
      :::note
      Forgot to close.
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "Unclosed directive 'note'"

  Scenario: Directives inside fenced code are not parsed
    Given the Markus source:
      """
      ```md
      :::note
      This is an example, not a callout.
      :::
      ```
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should not contain "markus-callout"
    And the HTML should contain ":::"
