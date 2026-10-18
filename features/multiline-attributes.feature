Feature: Multi-line directive attributes
  As an author with directives that carry several long attributes
  I want to spread the attribute block over multiple lines
  So that source stays readable without changing what a directive means

  Scenario: A leaf directive accepts an attribute block over several lines
    Given the Markus source:
      """
      ::metric{
        value="12"
        unit="ms"
        label="p95 latency"
      }
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain a "dl" with class "markus-metric"
    And the HTML should contain "p95 latency"

  Scenario: A container directive accepts an attribute block over several lines
    Given the Markus source:
      """
      :::card{
        title="Multi-line title"
        icon="bolt"
      }
      Card body.
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain "Multi-line title"
    And the HTML should contain "Card body."

  Scenario: Quoted values may contain both quote kinds and escaped quotes
    Given the Markus source:
      """
      ::metric{
        value="1"
        label="Two quote kinds: ' and \""
      }
      """
    When I parse the source
    Then the directive "metric" should have attribute "label" equal to the text:
      """
      Two quote kinds: ' and "
      """

  Scenario: A closing brace inside quotes does not end the block
    Given the Markus source:
      """
      ::metric{
        value="{braces} stay"
        label='a } inside'
      }
      """
    When I parse the source
    Then the directive "metric" should have attribute "value" equal to "{braces} stay"
    And the directive "metric" should have attribute "label" equal to "a } inside"

  Scenario: Content after a multi-line container head is parsed from the right line
    Given the Markus source:
      """
      :::card{
        title="Head"
      }
      Body text.
      :::

      ::metric{value="1" bogus="x"}
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "Unknown attribute"
    And the error should mention line 7

  Scenario: Single-line attribute blocks keep working
    Given the Markus source:
      """
      :::card{title="One line" icon="bolt"}
      Body.
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain "One line"

  Scenario: An unterminated attribute block is a clear error at the directive line
    Given the Markus source:
      """
      Intro.

      ::metric{
        value="1"
        label="never closed"
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "Unterminated attribute block"
    And the error should mention line 3

  Scenario: A malformed attribute reports the offending line and the directive line
    Given the Markus source:
      """
      ::metric{
        value="1"
        = broken
      }
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "attribute block starts at line 1"
    And the error should mention line 3

  Scenario: Strict attribute validation still applies to multi-line blocks
    Given the Markus source:
      """
      :::card{
        title="Fine"
        margin="2rem"
      }
      Body.
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "Unknown attribute"
    And the error should mention line 1

  Scenario: Attribute list lines inside a container still work
    Given the Markus source:
      """
      :::pull-quote{
        id="q"
      }
      > Measure what matters.
      {: attribution="Editorial principle" }
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain "Editorial principle"
