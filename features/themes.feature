Feature: Document themes
  As an author publishing Markus documents
  I want to apply themes such as hackerman
  So that documents render with cohesive palettes matching Antharchy / Omarchy

  Scenario: Front matter applies the hackerman theme to a full document
    Given the Markus source:
      """
      ---
      title: Cyberpunk Systems
      theme: hackerman
      ---

      # Terminal Access
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "hackerman"
    And the HTML should contain "--markus-ink: #ddf7ff"
    And the HTML should contain "--markus-paper: #0B0C16"
    And the HTML should contain "--markus-accent: #82FB9C"

  Scenario: Front matter applies the hackerman theme to an HTML fragment
    Given the Markus source:
      """
      ---
      title: Cyberpunk Systems
      theme: hackerman
      ---

      # Terminal Access
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "hackerman"

  Scenario: Theme can be specified via conversion option
    Given the Markus source:
      """
      # Terminal Access
      """
    When I convert the source to an HTML fragment with theme "hackerman"
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "hackerman"

  Scenario: CLI convert with --theme applies hackerman theme
    Given a Markus file "hacker.md" with:
      """
      # Cyberdeck Initialized
      """
    When I run "markus convert hacker.md --theme hackerman"
    Then the command should succeed
    And stdout should contain "hackerman"
    And stdout should contain "--markus-ink: #ddf7ff"

  Scenario: Unknown theme is rejected
    Given the Markus source:
      """
      ---
      title: Invalid Theme
      theme: non-existent-theme
      ---

      # Content
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "Unknown theme 'non-existent-theme'"

  Scenario: CLI rejects unknown theme
    Given a Markus file "test.md" with:
      """
      # Content
      """
    When I run "markus convert test.md --theme nonexistent"
    Then the command should fail
    And stderr should contain "Unknown theme 'nonexistent'"
