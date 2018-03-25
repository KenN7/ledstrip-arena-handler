import json

import experimentctrl as ec
# First test
JSON_TEST_1 = """
{
    "arena": {
        "edges": 3,
        "blocks": 2,
        "leds": 2,
        "color": "yellow",
        "brightness": 10,
        "edge": [
            {
                "index": 1,
                "color": "green",
                "block": [],
                "led":[]
            },
            {
                "index": 2,
                "color": "red",
                "block": [
                    {
                        "index": 1,
                        "color": "green",
                        "led": []
                    },
                    {
                        "index": 2,
                        "color": "omit",
                        "led": [
                            {
                                "index":1,
                                "color":"blue"
                            }
                        ]
                    }
                ],
                "led": []
            },
            {
                "index": 3,
                "color": "omit",
                "block": [],
                "led":[
                    {
                        "index":4,
                        "color":"blue"
                    }
                ]
            }
        ],
        "block": [
            {
                "index": 1,
                "color": "red",
                "led": []
            }
        ],
        "led": [
            {
                "index": 1,
                "color": "blue"
            },
            {
                "index": 2,
                "color": "red"
            }
        ]
    }
}
"""
# arena and edges working, including negatives
JSON_TEST_2 = """
{
    "arena": {
        "edges": 3,
        "blocks": 2,
        "leds": 2,
        "color": "red",
        "brightness": 10,
        "edge":[
            {"index":1,"color":"yellow","block":[],"led":[]},
            {"index":-1,"color":"blue","block":[],"led":[]}
        ],
        "block":[],
        "led":[]
    }
}
"""
# arena and blocks working, including negatives
JSON_TEST_3 = """
{
    "arena": {
        "edges": 3,
        "blocks": 2,
        "leds": 2,
        "color": "omit",
        "brightness": 10,
        "edge":[],
        "block":[
            {"index":1,"color":"yellow","led":[]},
            {"index":-4,"color":"blue","led":[]}
        ],
        "led":[]
    }
}
"""
# arena and leds working, including negatives
JSON_TEST_4 = """
{
    "arena": {
        "edges": 3,
        "blocks": 2,
        "leds": 2,
        "color": "omit",
        "brightness": 10,
        "edge":[],
        "block":[],
        "led":[
            {"index":1,"color":"yellow"},
            {"index":2,"color":"blue"}
        ]
    }
}
"""
# arena->block->led working, including negatives
JSON_TEST_5 = """
{
    "arena": {
        "edges": 1,
        "blocks": 1,
        "leds": 1,
        "color": "omit",
        "brightness": 10,
        "edge":[],
        "block":[
            {
                "index":1,"color":"white",
                "led":[
                    {"index":-1,"color":"yellow"},
                    {"index":-2,"color":"blue"},
                    {"index":-3,"color":"blue"},
                    {"index":-4,"color":"blue"},
                    {"index":-5,"color":"blue"},
                    {"index":-6,"color":"blue"},
                    {"index":-7,"color":"blue"},
                    {"index":-8,"color":"blue"},
                    {"index":-9,"color":"blue"},
                    {"index":-10,"color":"blue"},
                    {"index":-11,"color":"blue"},
                    {"index":-12,"color":"blue"}
                ]
            }
            ],
        "led":[]
    }
}
"""

if __name__ == "__main__":
    state = json.loads(JSON_TEST_5)
    ec.runState(state)
