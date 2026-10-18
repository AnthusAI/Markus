---
title: Conversation
description: conversation, message-group and message, role-labeled transcripts written as Markdown.
---

A conversation is a transcript of role-labeled messages, such as the request and response of a model API. Each message body is ordinary Markdown, so lists, emphasis and code need no HTML.

## Attributes

| Directive | Attribute | Values | Default |
| --- | --- | --- | --- |
| `conversation` | `title` | any text | `Conversation` for assistive technology |
| `conversation` | `kind` | `request`, `response` | none |
| `message-group` | `label` | any text (required) |  |
| `message` | `role` | any text (required) |  |

Every directive also accepts `id`, which becomes the HTML id; see [Syntax and metadata](demo-syntax.html#element-id).

A `conversation` holds `message` blocks, or `message-group` blocks that hold messages, never both. A `message` or `message-group` outside a conversation is a validation error.

## A request

:::example
```markus
:::conversation{title="request from application to OpenAI" kind="request"}
:::message{role="system"}
You are a helpful agent for an online store.
:::
:::message{role="user"}
Hello.
:::
:::
```
:::

## A response with a list and code

Message bodies are Markdown. Long code scrolls inside the message instead of widening the page.

:::example
````markus
:::conversation{title="response from OpenAI to the application" kind="response"}
:::message{role="assistant"}
Yes, the Sagrada Familia is in Barcelona. More specifically:

1. It is in the Eixample district.
2. Construction began in 1882 and **continues today**.

```python
model.invoke("Is the Sagrada Familia in Barcelona?").content
```
:::
:::
````
:::

## Groups of messages

A request often carries more than the history, such as the list of functions the model may call. Name each group with `label`.

:::example
```markus
:::conversation{title="request from application to OpenAI" kind="request"}
:::message-group{label="conversation history"}
:::message{role="system"}
You are a helpful agent for an online store.
:::
:::message{role="user"}
What's the status of order 123456789?
:::
:::
:::message-group{label="functions"}
:::message{role="check order status"}
Call this function with the order ID and it will give you the status of that order.
:::
:::message{role="create order"}
Call this function with the items and the customer's information to create an order.
:::
:::
:::
```
:::

## Free role names

The role is free text, so tools and functions keep their own names. The roles `system`, `user`, `assistant`, `tool` and `function` get their own accent color from the theme.

:::example
```markus
:::conversation{title="tool round trip"}
:::message{role="assistant"}
Call the "check order status" function for order ID 123456789.
:::
:::message{role="function"}
orderId: 123456789, status: 046-IN-TRANSIT, location: OAKLAND, CA
:::
:::
```
:::
