Feature: Conversation transcripts
  As an author explaining how a model API is called
  I want to write a request or response as a conversation of role-labeled messages
  So that transcripts are plain Markdown instead of hand-built HTML tables

  Scenario: A request renders as an ordered list of role-labeled messages
    Given the Markus source:
      """
      :::conversation{title="request from application to OpenAI" kind="request"}
      :::message{role="system"}
      You are a helpful agent for an online store.
      :::
      :::message{role="user"}
      Hello.
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain a "section" with class "markus-conversation--request"
    And the HTML should contain the markup:
      """
      aria-label="request from application to OpenAI"
      """
    And the HTML should contain ">request from application to OpenAI</p>"
    And the HTML should contain the markup:
      """
      <ol class="markus-messages">
      """
    And the HTML should contain a "li" with class "markus-message--system"
    And the HTML should contain the markup:
      """
      <span class="markus-message-role">system</span>
      """
    And the HTML should contain "You are a helpful agent for an online store."
    And the HTML should contain a "li" with class "markus-message--user"

  Scenario: Message bodies are ordinary Markdown including lists and code
    Given the Markus source:
      """
      :::conversation{kind="response"}
      :::message{role="assistant"}
      Yes, it is in **Barcelona**. More specifically:

      1. The Eixample district.
      2. The *Basilica*.

      ```python
      print("hello")
      ```
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain "<strong>Barcelona</strong>"
    And the HTML should contain "<li>The Eixample district.</li>"
    And the HTML should contain "print(&quot;hello&quot;)"
    And the HTML should contain a "section" with class "markus-conversation--response"

  Scenario: Messages can be grouped under a label such as functions
    Given the Markus source:
      """
      :::conversation{title="request" kind="request"}
      :::message-group{label="conversation history"}
      :::message{role="user"}
      What's the status of order 123456789?
      :::
      :::
      :::message-group{label="functions"}
      :::message{role="check order status"}
      Call this function with the order ID.
      :::
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain the markup:
      """
      role="group" aria-label="conversation history"
      """
    And the HTML should contain ">functions</p>"
    And the HTML should contain a "li" with class "markus-message--check-order-status"
    And the HTML should contain the markup:
      """
      <span class="markus-message-role">check order status</span>
      """

  Scenario: Role labels are free text and escaped
    Given the Markus source:
      """
      :::conversation
      :::message{role="tool <call>"}
      Result.
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should succeed
    And the HTML should contain "tool &lt;call&gt;"
    And the HTML should not contain "tool <call>"

  Scenario: A conversation rejects an unknown kind
    Given the Markus source:
      """
      :::conversation{kind="reply"}
      :::message{role="user"}
      Hi
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "kind"

  Scenario: A message needs a role
    Given the Markus source:
      """
      :::conversation
      :::message
      Hi
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "role"

  Scenario: A message must sit inside a conversation
    Given the Markus source:
      """
      :::message{role="user"}
      Hi
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "cannot appear"
    And the error should contain "conversation"

  Scenario: A conversation holds only messages
    Given the Markus source:
      """
      :::conversation
      Some prose.
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "may only contain"

  Scenario: A conversation needs at least one message
    Given the Markus source:
      """
      :::conversation{title="Empty"}
      :::message-group{label="nothing"}
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "at least one message"

  Scenario: A conversation cannot mix bare messages and groups
    Given the Markus source:
      """
      :::conversation
      :::message{role="user"}
      Hi
      :::
      :::message-group{label="functions"}
      :::message{role="f"}
      x
      :::
      :::
      :::
      """
    When I convert the source to an HTML fragment
    Then conversion should fail
    And the error should contain "cannot mix"
