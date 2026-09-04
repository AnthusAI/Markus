Feature: YAML front matter
  As a publisher
  I want document-level metadata at the top of a Markus file
  So that title, authors, and dates can drive HTML without polluting the body

  Scenario: Front matter becomes a document header
    Given the Markus source:
      """
      ---
      title: Local inference
      authors:
        - Ada
        - Gus
      date: 2026-09-04
      description: A brief on running models nearby.
      ---

      The body starts here.
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain "<h1>Local inference</h1>"
    And the HTML should contain "Ada, Gus"
    And the HTML should contain "2026-09-04"
    And the HTML should contain "A brief on running models nearby."
    And the HTML should contain "The body starts here."

  Scenario: Front matter is available on the AST
    Given the Markus source:
      """
      ---
      title: Brief
      template: editorial
      ---

      Hello.
      """
    When I parse the source
    Then the front matter key "title" should be "Brief"
    And the front matter key "template" should be "editorial"

  Scenario: Documents without front matter still parse
    Given the Markus source:
      """
      Just a paragraph.
      """
    When I parse the source
    Then the document should have empty front matter
    And the document should contain markdown starting with "Just a paragraph."
