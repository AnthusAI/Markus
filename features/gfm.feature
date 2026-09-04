Feature: GitHub Flavored Markdown baseline
  As a writer who already uses GitHub Markdown
  I want Markus to accept ordinary GFM without ceremony
  So that directives are an opt-in layout vocabulary, not a new dialect of paragraphs

  Scenario: Headings, emphasis, and fenced code render as GFM
    Given the Markus source:
      """
      # Title

      This is **bold** and *italic* and `code`.

      ```python
      print("ok")
      ```
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain "<h1>Title</h1>"
    And the HTML should contain "<strong>bold</strong>"
    And the HTML should contain "<em>italic</em>"
    And the HTML should contain "<code>code</code>"
    And the HTML should contain "print(&quot;ok&quot;)"

  Scenario: Tables and strikethrough
    Given the Markus source:
      """
      | Keep | Move |
      | --- | --- |
      | intent | CSS |

      This is ~~obsolete~~.
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain "<table>"
    And the HTML should contain "<th>Keep</th>"
    And the HTML should contain "<td>intent</td>"
    Then the HTML should contain struck text "obsolete"

  Scenario: Task lists
    Given the Markus source:
      """
      - [x] done
      - [ ] todo
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain "checkbox"
    And the HTML should contain "todo"

  Scenario: Autolinks
    Given the Markus source:
      """
      See https://github.com/AnthusAI/Markus for the source.
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain a link to "https://github.com/AnthusAI/Markus"

  Scenario: Raw HTML is disabled by default
    Given the Markus source:
      """
      <script>alert(1)</script>
      """
    When I convert the source to an HTML fragment
    Then the HTML should not contain "<script>"
