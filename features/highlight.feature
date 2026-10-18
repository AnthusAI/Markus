Feature: Highlighted text
  As an author
  I want to mark a phrase with double equals signs
  So that emphasis-by-highlight is plain text instead of raw mark tags

  Scenario: Double equals highlight a phrase
    Given the Markus source:
      """
      A preview of ==a new type of software solution.==
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain "<mark>a new type of software solution.</mark>"
    And the HTML should not contain "=="

  Scenario: Emphasis nests inside a highlight
    Given the Markus source:
      """
      ==**Run the counterfactual as a smoke test.**==
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain "<mark><strong>Run the counterfactual as a smoke test.</strong></mark>"

  Scenario: A highlight can sit inside emphasis and around a link
    Given the Markus source:
      """
      *see ==the [docs](https://example.com/docs) page==*
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain the markup:
      """
      <em>see <mark>the <a href="https://example.com/docs">docs</a> page</mark></em>
      """

  Scenario: A highlight can span lines inside a paragraph
    Given the Markus source:
      """
      before ==the first line
      and the second line== after
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain "<mark>the first line"
    And the HTML should contain "and the second line</mark> after"

  Scenario: Several highlights in one paragraph stay separate
    Given the Markus source:
      """
      ==one== and ==two==
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain "<mark>one</mark> and <mark>two</mark>"

  Scenario: Code is never highlighted
    Given the Markus source:
      """
      Use `a ==b== c` literally.

      ```python
      if a ==b== c:
          pass
      ```
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain "<code>a ==b== c</code>"
    And the HTML should contain "if a ==b== c:"
    And the HTML should not contain "<mark>"

  Scenario: An unmatched or spaced marker stays literal text
    Given the Markus source:
      """
      x == y and a ==  b == c and ==dangling
      """
    When I convert the source to an HTML fragment
    Then the HTML should not contain "<mark>"
    And the HTML should contain "x == y"

  Scenario: Highlights work in headings and table cells
    Given the Markus source:
      """
      ## A ==marked== heading

      | a |
      | --- |
      | ==cell== |
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain "<mark>marked</mark>"
    And the HTML should contain "<mark>cell</mark>"

  Scenario: Highlights appear in the document IR
    Given the Markus source:
      """
      say ==this== now
      """
    When I parse the source into the document IR
    Then the document IR child 0 inline text should be "say this now"
