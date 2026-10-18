Feature: Source and preview examples
  As a documentation author
  I want to show a Markus snippet beside the page it renders
  So that readers see the source and the result together, from one copy of the source

  Scenario: An example renders its source and its preview
    Given the Markus source:
      """
      :::example
      ```markus
      :::callout{kind="tip"}
      Keep the source diffable.
      :::
      ```
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain a "figure" with class "markus-example"
    And the HTML should contain a "div" with class "markus-example-source"
    And the HTML should contain a "div" with class "markus-example-preview"
    And the HTML should contain "Keep the source diffable."
    And the HTML should contain a "aside" with class "markus-callout markus-callout--tip"
    And the HTML should contain the markup:
      """
      <span class="markus-src-fence">:::</span><span class="markus-src-name">callout</span><span class="markus-src-attrs">{kind=&quot;tip&quot;}</span>
      """

  Scenario: The source pane shows the snippet exactly as written
    Given the Markus source:
      """
      :::example
      ```md
      Some **bold** text & a <tag>.
      ```
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain "Some **bold** text &amp; a &lt;tag&gt;."
    And the HTML should contain "<strong>bold</strong>"

  Scenario: Examples sit side by side by default
    Given the Markus source:
      """
      :::example
      ```markus
      Hello.
      ```
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain the markup:
      """
      data-layout="side-by-side"
      """

  Scenario: An example can ask to stack source above preview
    Given the Markus source:
      """
      :::example{layout="stacked" title="A wide layout"}
      ```markus
      Hello.
      ```
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain the markup:
      """
      data-layout="stacked"
      """
    And the HTML should contain the markup:
      """
      <figcaption class="markus-example-title">A wide layout</figcaption>
      """

  Scenario: Code fences inside an example use a longer outer fence
    Given the Markus source:
      """
      :::example
      ````markus
      ```python
      print("hi")
      ```
      ````
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain "```python"
    And the HTML should contain the markup:
      """
      <code class="language-python">
      """

  Scenario: Front matter in an example renders the document header
    Given the Markus source:
      """
      :::example
      ```markus
      ---
      title: Field notes
      description: A short report.
      ---

      Body text.
      ```
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain "<h1>Field notes</h1>"
    And the HTML should contain "A short report."

  Scenario: An example must hold exactly one code fence
    Given the Markus source:
      """
      :::example
      Just a paragraph.
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "must contain exactly one fenced code block"

  Scenario: Invalid Markus inside an example fails the build at the right line
    Given the Markus source:
      """
      Intro.

      :::example
      ```markus
      Fine.

      :::callout{kind="loud"}
      Nope.
      :::
      ```
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "kind"
    And the error should mention line 7

  Scenario: Unknown example attributes are errors
    Given the Markus source:
      """
      :::example{columns=2}
      ```markus
      Hello.
      ```
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
