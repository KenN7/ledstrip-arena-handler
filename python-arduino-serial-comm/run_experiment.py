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
        "brightness": 25,
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
# arena and edges working, including negatives, verificar brillo
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
        "edge":[{"index":1,"color":"yellow","block":[],"led":[]}],
        "block":[],
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
        "color": "red",
        "brightness": 10,
        "edge":[
            {"index":-1,"color":"yellow","block":[],"led":[]},
            {"index":2,"color":"omit","block":[],"led":[{"index":1,"color":"white"}]},
            {"index":3,"color":"omit","block":[{"index":-1,"color":"white","led":[{"index":3,"color":"green"}]}],"led":[]}
        ],
        "block":[{"index":2,"color":"blue","led":[{"index":1,"color":"white"}]}],
        "led":[{"index":1,"color":"yellow"}]
    }
}
"""
# arena->block->led working, including negatives # se corrio led
JSON_TEST_5 = """
{
    "arena": {
        "edges": 3,
        "blocks": 2,
        "leds": 2,
        "color": "omit",
        "brightness": 10,
        "edge":[],
        "block":[
            {
                "index":2,"color":"white",
                "led":[
                    {"index":1,"color":"yellow"},
                    {"index":2,"color":"blue"}
                ]
            }
            ],
        "led":[]
    }
}
"""
# arena and leds working, range test
JSON_TEST_6 = """
{
    "arena": {
        "edges": 3,
        "blocks": 2,
        "leds": 2,
        "color": "omit",
        "brightness": 5,
        "edge":[
            {"index":[-3,1],"color":"yellow","block":[],"led":[]}
        ],
        "block":[{"index":[-1,4],"color":"blue","led":[]}],
        "led":[]
    }
}
"""

if __name__ == "__main__":
    state = json.loads(JSON_TEST_6)
    ec.runState(state)
