# TAPython_ChatGTP_UE5

This is a demo project of using ChatGPT to create Slate UI with TAPython in Unreal Engine 5. 

TAPython uses JSON for the user interface, which is friendly with ChatGPT.

demo video: https://www.youtube.com/watch?v=H3MjtmX58IQ

## Menu entry item

./UI/MenuConfig.json

```json
    "OnToolBarChameleon": {
        "name": "Python Chameleon on toolbar",
        "items": [
            {
                "name": "Chat GPT Demo",
                "ChameleonTools": "../Python/Chats/Chat.json"
            }
        ]
    }
    ...
```

