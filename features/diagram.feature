Feature: Flow diagrams
  As an author explaining how parts of a system relate
  I want to describe boxes and the arrows between them in Markdown
  So that diagrams are accessible HTML with theme colors instead of hand-styled divs

  Scenario: Nodes and a two-way link render as an ordered flow
    Given the Markus source:
      """
      :::diagram{title="The Cybernetic Loop"}
      :::node{title="Engine" tone="agent"}
      LLM generation. Fast, prolific, tireless.
      :::
      ::link{label="output" back="correction"}
      :::node{title="Governor"}
      Specs, tests, CI gates, telemetry.
      :::
      Skip the loop and it stops being cybernetic: it is just an Engine running open, *vibe coding*.
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain the markup:
      """
      <figure class="markus-diagram" role="group" aria-label="The Cybernetic Loop">
      """
    And the HTML should contain the markup:
      """
      <p class="markus-diagram-title">The Cybernetic Loop</p>
      """
    And the HTML should contain the markup:
      """
      <ol class="markus-diagram-flow">
      """
    And the HTML should contain a "li" with class "markus-diagram-node--agent"
    And the HTML should contain a "li" with class "markus-diagram-node--neutral"
    And the HTML should contain the markup:
      """
      <p class="markus-diagram-node-title">Engine</p>
      """
    And the HTML should contain "LLM generation. Fast, prolific, tireless."
    And the HTML should contain a "li" with class "markus-diagram-link"
    And the HTML should contain the markup:
      """
      <p class="markus-diagram-link-forward"><span aria-hidden="true">&darr;</span>
      """
    And the HTML should contain the markup:
      """
      <span class="markus-visually-hidden">Feeds back: </span>correction
      """
    And the HTML should contain the markup:
      """
      <figcaption class="markus-diagram-caption"><p>Skip the loop
      """
    And the HTML should contain "<em>vibe coding</em>"

  Scenario: A row places nodes side by side
    Given the Markus source:
      """
      :::diagram{title="Two Minds, Two Systems"}
      :::row
      :::node{title="System 1" tone="agent"}
      Fast, intuitive, pattern-matching.
      :::
      :::node{title="System 2" tone="human"}
      Slow, deliberate, logical.
      :::
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain the markup:
      """
      <li class="markus-diagram-row"><ul class="markus-diagram-row-items">
      """
    And the HTML should contain a "li" with class "markus-diagram-node--agent"
    And the HTML should contain a "li" with class "markus-diagram-node--human"

  Scenario: Links connect a row to the node above and below
    Given the Markus source:
      """
      :::diagram
      :::node{title="Human" tone="human"}
      :::
      ::link{label="assigns and checks work"}
      :::row
      :::node{title="Coding agent" tone="agent"}
      :::
      :::node{title="Coding agent" tone="agent"}
      :::
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain the markup:
      """
      <figure class="markus-diagram" role="group" aria-label="Diagram">
      """
    And the HTML should contain "assigns and checks work"
    And the HTML should not contain "markus-diagram-link-back"
    And the HTML should not contain "markus-diagram-node-body"

  Scenario: A link may be a bare arrow
    Given the Markus source:
      """
      :::diagram
      :::node{title="A"}
      :::
      ::link
      :::node{title="B"}
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain the markup:
      """
      <span class="markus-visually-hidden">Then</span>
      """

  Scenario: Node text is escaped and bodies are Markdown
    Given the Markus source:
      """
      :::diagram
      :::node{title="<script>"}
      - one
      - two **bold**
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain "&lt;script&gt;"
    And the HTML should contain "<li>two <strong>bold</strong></li>"

  Scenario: Tone is a fixed semantic set and never a color
    Given the Markus source:
      """
      :::diagram
      :::node{title="Bad" tone="#F7E8EA"}
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "tone"
    And the error should mention line 2

  Scenario Outline: Every tone renders its own class
    Given the Markus source:
      """
      :::diagram
      :::node{title="Box" tone="<tone>"}
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain a "li" with class "markus-diagram-node--<tone>"

    Examples:
      | tone    |
      | neutral |
      | human   |
      | agent   |
      | risk    |
      | ok      |

  Scenario: A node needs a title
    Given the Markus source:
      """
      :::diagram
      :::node
      Text
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "title"

  Scenario: A node must sit inside a diagram or row
    Given the Markus source:
      """
      :::node{title="Loose"}
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "must be placed inside"

  Scenario: A diagram needs a node
    Given the Markus source:
      """
      :::diagram{title="Empty"}
      Only a caption.
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "at least one node or row"

  Scenario: A link cannot be first or last
    Given the Markus source:
      """
      :::diagram
      ::link{label="start"}
      :::node{title="A"}
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "between two nodes"

  Scenario: Two links cannot touch
    Given the Markus source:
      """
      :::diagram
      :::node{title="A"}
      :::
      ::link
      ::link
      :::node{title="B"}
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "between two nodes"

  Scenario: Prose between nodes is rejected so the caption stays last
    Given the Markus source:
      """
      :::diagram
      :::node{title="A"}
      :::
      Stray prose.
      :::node{title="B"}
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "caption"

  Scenario: A row holds only nodes
    Given the Markus source:
      """
      :::diagram
      :::row
      ::link
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "cannot appear inside 'row'"

  Scenario: A row needs at least one node
    Given the Markus source:
      """
      :::diagram
      :::row
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "at least one node"

  Scenario: A row cannot nest in a row
    Given the Markus source:
      """
      :::diagram
      :::row
      :::row
      :::
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "cannot appear inside 'row'"
