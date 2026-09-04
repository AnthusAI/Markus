Feature: Semantic layout directives
  As a writer of technical explainers
  I want colon-fenced blocks that name intent
  So that a renderer can produce accessible layout without CSS in the source

  Scenario: A pull quote becomes a figure with attribution
    Given the Markus source:
      """
      :::pull-quote{attribution="Engineering principle" tone="primary"}
      The best system is often the one whose failure modes you can explain.
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain a "figure" with class "markus-pull-quote"
    And the HTML should contain a "figure" with class "markus-pull-quote--primary"
    And the HTML should contain "<figcaption>Engineering principle</figcaption>"
    And the HTML should contain "failure modes"

  Scenario: Inline attribute lists are lifted onto the directive
    Given the Markus source:
      """
      :::pull-quote
      > Measure what matters.
      {: attribution="Editorial principle" tone="quiet" }
      :::
      """
    When I parse the source
    Then the directive "pull-quote" should have attribute "attribution" equal to "Editorial principle"
    And the directive "pull-quote" should have attribute "tone" equal to "quiet"

  Scenario: Callout kinds render as asides
    Given the Markus source:
      """
      :::callout{kind="warning" title="Watch this"}
      Do not put `margin` in the source.
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain a "aside" with class "markus-callout--warning"
    And the HTML should contain "Watch this"
    And the HTML should contain "<code>margin</code>"

  Scenario Outline: Callout aliases set the kind
    Given the Markus source:
      """
      :::<alias>
      Body.
      :::
      """
    When I parse the source
    Then the directive "callout" should have attribute "kind" equal to "<kind>"

    Examples:
      | alias   | kind    |
      | note    | note    |
      | warning | warning |
      | tip     | tip     |
      | caution | caution |

  Scenario: Feature cards nest inside a feature grid
    Given the Markus source:
      """
      :::feature-grid{columns=3 label="Core principles"}
      :::feature-card{icon="bolt"}
      ## Low latency
      Keep work local.
      :::
      :::feature-card{icon="lock"}
      ## Private by default
      Transmit only what the task needs.
      :::
      :::feature-card{icon="gauge"}
      ## Measurable cost
      Track tokens and watts.
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain a "section" with class "markus-card-grid"
    And the HTML should contain an attribute aria-label of "Core principles"
    And the HTML should contain "Low latency"
    And the HTML should contain "Private by default"
    And the HTML should contain "Measurable cost"
    And the HTML should contain three "article" elements with class "markus-card"

  Scenario: Two-up requires a pair of columns
    Given the Markus source:
      """
      :::two-up{ratio="2:1"}
      :::column
      ## What changes
      Marginal cost falls.
      :::
      :::column
      ## What remains
      Evaluation still matters.
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain a "section" with class "markus-two-up"
    And the HTML should contain an attribute data-ratio of "2:1"
    And the HTML should contain "What changes"
    And the HTML should contain "What remains"

  Scenario: Figure with media attributes
    Given the Markus source:
      """
      :::figure{src="diagram.svg" alt="A flow" caption="The pipeline" credit="Anthus"}
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain an attribute src of "diagram.svg"
    And the HTML should contain an attribute alt of "A flow"
    And the HTML should contain "The pipeline"
    And the HTML should contain "Anthus"

  Scenario: Details and aside
    Given the Markus source:
      """
      :::details{summary="More" open=true}
      Hidden on purpose.
      :::

      :::aside{title="By the way"}
      Supporting material.
      :::
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain "<details"
    And the HTML should contain " open"
    And the HTML should contain "<summary>More</summary>"
    And the HTML should contain a "aside" with class "markus-aside"
    And the HTML should contain "Supporting material"

  Scenario: Metric is a leaf directive
    Given the Markus source:
      """
      ::metric{value="12" unit="ms" label="p95 latency" delta="-8%"}
      """
    When I convert the source to an HTML fragment
    Then the HTML should contain a "dl" with class "markus-metric"
    And the HTML should contain "p95 latency"
    And the HTML should contain "12"
    And the HTML should contain "ms"
    And the HTML should contain "-8%"
