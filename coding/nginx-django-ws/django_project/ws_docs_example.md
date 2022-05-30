## The endpoint
`wss://casamsa.ga/ws/chat/`

 - [methods](#methods)
 - [events](#events)
 - [data types](#data-types)

## Methods
### Common structure of the methods
```js
{
    method: "method_name",
    access_token: "token",
    args: {
        key: "value",
        event_response_key: null  // optional
    }
}

```
methods:
 - [auth](#auth)
 - [create_chat](#create_chat)
 - [update_chat](#update_chat)
 - [send_message](#send_message)
 - [read_messages](#read_messages)
 - [remove_from_chat](#remove_from_chat)
 - [add_to_chat](#add_to_chat)

#### event_response_key
All methods have optional `event_response_key` argument, that can be used to pass any data.

Then, when you have event-response (for example, [message_created](#message_created)), you can obtain the data you have passed.
#### access_token
Here you can pass the token. It is not required for each request - the channel will be authorized with the first successful one.
### auth
Call it when you need to authenticate the channel but want not to call other methods.

> Request structure:
```js
{
    method: "auth"
}
```

### create_chat
> Request structure:
```js
{
    method: "create_chat",
    args: {
        users: [
            1,
            2
        ],
        title: "title" | null  // not required
    }
}
```
 - > Related: [chat_duplication_error](#chat_duplication_error)

### update_chat
> Request structure:
```js
{
    method: "update_chat",
    args: {
        chat: 1,
        title: "title" | null
    }
}
```
 - > Related: [chat_updated](#chat_updated)

### send_message
Can have both text and files or one of them.

> Request structure:
```js
{
    method: "send_message",
    args: {
        chat: 1,
        text: "string",
        files: [ 
            {
                name: "string",
                data: "base64 string"
            }
        ]
    }
}
```

### read_messages
Sets the read status for all messages.

New statuses will be sent with [messages_updated](#messages_updated) event

> Request structure:
```js
{
    method: "read_messages",
    args: {
        chat: 1
    }
}
```
 - > Related: [messages_read](#messages_read) event

### remove_from_chat
Removes given users from the chat

> Request structure:
```js
{
    method: "remove_from_chat",
    args: {
        users: [1],
        chat: 1
    }
}
```
 - > Related: [user_removed_successful](#user_removed_successful) | [user_removed](#user_removed) | [chat_removed](#chat_removed)

### add_to_chat
Adds given users to the chat

> Request structure:
```js
{
    method: "add_to_chat",
    args: {
        users: [1],
        chat: 1
    }
}
```
 - > Related: [user_added_successful](#user_added_successful) | [user_added](#user_added)

## Events
### Common structure of the events
```js
{
    type: "event_name",
    data: {
        key: "value"
    }
}
```
types:
 - [error](#error)
 - [authenticated](#authenticated)
 - [new_chat](#new_chat)
 - [new_message](#new_message)
 - [message_created](#message_created)
 - [messages_read](#messages_read)
 - [chat_created](#chat_created)
 - [messages_updated](#messages_updated)
 - [user_removed_successful](#user_removed_successful)
 - [user_removed](#user_removed)
 - [user_added_successful](#user_added_successful)
 - [user_added](#user_added)
 - [chat_updated](#chat_updated)
 - [chat_removed](#chat_removed)

### error
> Event structure:
```js
{
    type: "error",
    data: {
        type: "error_type",
        detail: "error details",
        event_response_key: null
    }
}
```
error types and their addition fields:
 - `system_error`
 - `access_error`
 - `authorization_error`
 - `field_error`
 - `chat_duplication_error`
```js
type: "chat_duplication_error",
//...
chat_id: 1
```

### authenticated
Fires after successful [`auth`](#auth) execution.

> Event structure:
```js
{
    type: "authenticated",
    data: {
        event_response_key: null
    }
}
```

### new_message
Fires when a new message obtained (in any of chats that the user belong to).

> Event structure:
```js
{
    type: "new_message",
    data: {
        message: Message
    }
}
```

### new_chat
Fires a chat with the user created (or user have been added to the chat), but not by the user itself - like invitation.

> Event structure:
```js
{
    type: "new_chat",
    data: {
        chat: Chat
    }
}
```

### message_created
Fires when a new message successfully created by the user

> Event structure:
```js
{
    type: "message_created",
    data: {
        message: Message,
        event_response_key: null
    }
}
```

### messages_read
Fires when messages have been successfully read

> Event structure:
```js
{
    type: "messages_read",
    data: {
        chat: 1
    }
}
```

### chat_created
Fires when a new chat successfully created by the user

> Event structure:
```js
{
    type: "chat_created",
    data: {
        chat: Chat,
        event_response_key: null
    }
}
```

### messages_updated
Fires when there are new updates for messages

> Event structure:
```js
{
    type: "messages_updated",
    data: {
        updates: [
            {
                id: 1,
                fields: {
                    // some fields of the Message
                }
            }
        ]
    }
}
```
#### Fields can be updated for now:
 - `is_read`

### user_removed_successful
Fires after successful [`remove_from_chat`](#remove_from_chat) execution. Receive: initiator

> Event structure:
```js
{
    type: "user_removed_successful",
    data: {
        'event_response_key': null,
        'user_ids': [1],
        'chat': Chat
    }
}
```

### user_removed
Fires after successful [`remove_from_chat`](#remove_from_chat) execution. Receive: other chat members

> Event structure:
```js
{
    type: "user_removed",
    data: {
        'user_ids': [1],
        'chat': Chat
    }
}
```

### user_added_successful
Fires after successful [`add_to_chat`](#add_to_chat) execution. Receive: initiator

> Event structure:
```js
{
    type: "user_added_successful",
    data: {
        'event_response_key': null,
        'user_ids': [1],
        'chat': Chat
    }
}
```

### user_added
Fires after successful [`add_to_chat`](#add_to_chat) execution. Receive: other chat members

> Event structure:
```js
{
    type: "user_added",
    data: {
        'user_ids': [1],
        'chat': Chat
    }
}
```

### chat_updated
Fires when there are new updates for a chat. Receive: chat members

> Event structure:
```js
{
    type: "chat_updated",
    data: {
        chat: Chat
    }
}
```

### chat_removed
Fires when the user's been removed from given chat (or chat's been removed itself). Receive: removed user

> Event structure:
```js
{
    type: "chat_removed",
    data: {
        chat: Chat
    }
}
```


## Data Types
 - [Chat](#chat)
 - [Message](#message)
 - [File](#file)
 - [User](#user)

### Chat
```js
{
    id: 1,
    users: [
        User
    ],
    title: "title",
    created_at: "time",
    updated_at: "time"
}
```

### Message
```js
{
    id: 1,
    chat: 1,
    user: User,
    attached_files: [
        File
    ],
    text: "string",
    created_at: "time",
    updated_at: "time",
    is_read: true
}
```

### File
```js
{
    id: 1,
    name: "string",
    file: "https://url",
    created_at: "time"
}
```

### User
```js
{
    pk: 0,
    email: "user@example.com",
    first_name: "string",
    last_name: "string",
    photo: "https://url",
    color: "#hex",
    role: "Member"
}
```