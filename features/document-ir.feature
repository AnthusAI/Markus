Feature: Document intermediate representation
  As a downstream consumer of Markus content (e.g. a layout engine)
  I want a fully typed document tree, not opaque raw-Markdown strings
  So that I can consume block-level structure without re-parsing Markdown myself

  Scenario: The document IR carries a schema version
    Given the Markus source:
      """
      Hello.
      """
    When I parse the source into the document IR
    Then the document IR schema_version should be 1

  Scenario: A heading becomes a typed heading node
    Given the Markus source:
      """
      ## A Heading
      """
    When I parse the source into the document IR
    Then the document IR child 0 type should be "heading"
    And the document IR child 0 field "level" should equal 2
    And the document IR child 0 inline text should be "A Heading"

  Scenario: A paragraph becomes a typed paragraph node
    Given the Markus source:
      """
      Just a sentence.
      """
    When I parse the source into the document IR
    Then the document IR child 0 type should be "paragraph"
    And the document IR child 0 inline text should be "Just a sentence."

  Scenario: A bullet list becomes a typed list node with items
    Given the Markus source:
      """
      - alpha
      - beta
      - gamma
      """
    When I parse the source into the document IR
    Then the document IR child 0 type should be "list"
    And the document IR child 0 field "ordered" should equal false
    And the document IR child 0 should have 3 "items" entries

  Scenario: An ordered list records its starting number
    Given the Markus source:
      """
      5. five
      6. six
      """
    When I parse the source into the document IR
    Then the document IR child 0 type should be "list"
    And the document IR child 0 field "ordered" should equal true
    And the document IR child 0 field "start" should equal 5

  Scenario: A GFM task list item records its checked state
    Given the Markus source:
      """
      - [x] done
      - [ ] todo
      """
    When I parse the source into the document IR
    Then the document IR child 0 item 0 checked should be true
    And the document IR child 0 item 1 checked should be false

  Scenario: A blockquote becomes a typed blockquote node containing block children
    Given the Markus source:
      """
      > A quoted paragraph.
      """
    When I parse the source into the document IR
    Then the document IR child 0 type should be "blockquote"
    And the document IR child 0 should have 1 "children" entries

  Scenario: A fenced code block records its language
    Given the Markus source:
      """
      ```python
      print("hi")
      ```
      """
    When I parse the source into the document IR
    Then the document IR child 0 type should be "code"
    And the document IR child 0 field "lang" should equal "python"

  Scenario: A thematic break becomes a typed node
    Given the Markus source:
      """
      Above.

      ---

      Below.
      """
    When I parse the source into the document IR
    Then the document IR child 1 type should be "thematic_break"

  Scenario: A table becomes a typed table node
    Given the Markus source:
      """
      | Keep | Move |
      | --- | --- |
      | intent | CSS |
      """
    When I parse the source into the document IR
    Then the document IR child 0 type should be "table"
    And the document IR child 0 should have 2 "header" entries
    And the document IR child 0 should have 1 "rows" entries

  Scenario: Directives and Markdown blocks are ordered peers
    Given the Markus source:
      """
      # Title

      A first paragraph.

      :::pull-quote{attribution="R"}
      Quoted.
      :::

      A second paragraph.
      """
    When I parse the source into the document IR
    Then the document IR children types should be:
      | type      |
      | heading   |
      | paragraph |
      | directive |
      | paragraph |

  Scenario: Markdown nested inside a directive is also exploded into typed peers
    Given the Markus source:
      """
      :::callout{kind="note"}
      ## Nested heading

      Nested paragraph.
      :::
      """
    When I parse the source into the document IR
    Then the document IR child 0 type should be "directive"
    And the document IR child 0 should have 2 "children" entries

  Scenario: Raw HTML stays plain text by default and typed when allowed
    Given the Markus source:
      """
      <div>raw</div>
      """
    When I parse the source into the document IR
    Then the document IR child 0 type should be "paragraph"
    When I parse the source into the document IR with html allowed
    Then the document IR child 0 type should be "html"

  Scenario: markus ast prints the same typed structure as JSON
    Given a Markus file "typed.md" with:
      """
      # Title

      A paragraph.
      """
    When I run "markus ast typed.md"
    Then the command should succeed
    And the ast JSON output children types should be:
      | type      |
      | heading   |
      | paragraph |
    And the ast JSON output schema_version should be 1
