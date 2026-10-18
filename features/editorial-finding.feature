Feature: Editorial finding markup
  As a copy editor or downstream tool
  I want a standard Markus directive for diagnostic findings
  So annotated Markdown stays portable and validated

  Scenario: An editorial finding renders with metadata
    Given the Markus source:
      """
      :::editorial-finding{id="finding-0123456789abcdef" kind="voice_mismatch" rationale="Passive construction"}
      The Researcher checked whether the problem had been solved.
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain a "aside" with class "markus-editorial-finding"
    And the HTML should contain "finding-0123456789abcdef"
    And the HTML should contain "voice_mismatch"
    And the HTML should contain "Passive construction"
    And the HTML should contain "problem had been solved"

  Scenario: Editorial finding attributes are validated
    Given the Markus source:
      """
      :::editorial-finding{id="not-a-finding-id" kind="empty_leadin"}
      Bad id.
      :::
      """
    When I parse the source
    Then conversion should fail
