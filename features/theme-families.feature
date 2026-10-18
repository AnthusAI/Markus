Feature: Theme families with light and dark palettes
  As a reader
  I want a themed page to follow my light or dark setting
  So that a theme never forces a dark page on me in daylight, or the reverse

  Scenario: A theme family carries both palettes and follows the system setting
    Given the Markus source:
      """
      ---
      title: Field notes
      theme: solarized
      ---

      Body text.
      """
    When I convert the source to a full HTML document
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "solarized"
    And the HTML should contain "--markus-paper: #fdf6e3"
    And the HTML should contain "--markus-paper: #002b36"
    And the HTML should contain "@media (prefers-color-scheme: dark)"

  Scenario: A root data-color-scheme attribute forces one palette
    Given the Markus source:
      """
      # Body
      """
    When I convert the source to a full HTML document
    Then the HTML should contain the markup:
      """
      :root[data-color-scheme="dark"] [data-theme="solarized"]
      """
    And the HTML should contain the markup:
      """
      :root:not([data-color-scheme="light"]) [data-theme="solarized"]
      """

  Scenario Outline: Every theme family is available by name
    Given the Markus source:
      """
      ---
      theme: <theme>
      ---

      Body text.
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain an attribute data-theme of "<theme>"

    Examples:
      | theme       |
      | solarized   |
      | catppuccin  |
      | everforest  |
      | flexoki     |
      | github      |
      | gruvbox     |
      | kanagawa    |
      | one         |
      | rose-pine   |
      | tokyo-night |

  Scenario: Every bundled theme declares exactly the color modes it is registered with
    Then every bundled theme stylesheet matches its registered color modes
