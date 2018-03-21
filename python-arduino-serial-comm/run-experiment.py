import json

from ArduinoInstruction import ArduinoInstruction
from Arena import Arena
from Edge import Edge
from Block import Block
from Led import Led
from BlockInstruction import BlockInstruction
from Color import Color

JSON_TEST = """
{
    "arena": {
        "edges": 3,
        "blocks": 2,
        "leds": 2,
        "color": "omit",
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


def generateArdInsForArena(arena):
    print(
        "Arena: %d, %d, %d, %s"
        % (arena.edges, arena.blocks, arena.leds, arena.color)
    )
    aIns = ArduinoInstruction('COM4', 57600)
    aIns.start_connection()
    for i in range(0, (arena.blocks * arena.edges)):
        bIns = BlockInstruction()
        bIns.brightness = arena.brightness
        bIns.block = \
            str(i) + "," \
            + str(arena.leds) + "," \
            + Color[arena.color.upper()].value
        aIns.send_instrunction(str(bIns.toJSON()))
    generateArdInsForEdge(arena.edge, arena, aIns)
    #generateArdInsForBlock(arena.block, arena, aIns)
    #generateArdInsForLed(arena.led, arena, aIns)
    aIns.close_connection()


def generateArdInsForEdge(edges, arena, aIns):

    for jsonEdge in edges:
        edge = Edge(json.dumps(jsonEdge))
        # Converting from negative to equivalent positive
        edge.index = \
            arena.edges + edge.index + 1 if (edge.index < 0) else edge.index
        #
        print("Edge: %s, %d, %a" % (edge.color, edge.index, edge.block))
        for i in range(-1, (arena.blocks - 1)):
            bIns = BlockInstruction()
            bIns.brightness = 25
            bIns.block = \
                str((edge.index * arena.blocks + i) - 1) + "," \
                + str(arena.leds) + "," \
                + Color[edge.color.upper()].value
            aIns.send_instrunction(str(bIns.toJSON()))
        # If there are some blocks, execute them.
        for jsonBlock in edge.block:
            jsonBlock['index'] = \
                edgeBlockToBlock(edge.index, arena.blocks, jsonBlock['index'])
        generateArdInsForBlock(edge.block, arena, aIns)
        # If there are some leds, execute them.
        for jsonLed in edge.led:
            jsonLed['index'] = \
                edgeBlockToBlock(
                    edge.index, (arena.blocks * arena.leds), jsonLed['index']
            )
        generateArdInsForLed(edge.led, arena, aIns)


def generateArdInsForBlock(blocks, arena, aIns):
    for jsonBlock in blocks:
        block = Block(json.dumps(jsonBlock))
        # Converting from negative to equivalent positive
        block.index = \
            (arena.blocks * arena.edges) + block.index + 1\
            if (block.index < 0) else block.index
        #
        print("Block: %s, %d, %a" % (block.color, block.index, block.led))
        bIns = BlockInstruction()
        bIns.brightness = arena.brightness
        bIns.block = \
            str(block.index - 1) + "," \
            + str(arena.leds) + "," \
            + Color[block.color.upper()].value
        aIns.send_instrunction(str(bIns.toJSON()))
        # If there are some leds, execute them.
        for jsonLed in block.led:
            jsonLed['index'] = \
                edgeBlockToBlock(
                    block.index, arena.leds, jsonLed['index']
            )
        generateArdInsForLed(block.led, arena, aIns)


def generateArdInsForLed(leds, arena, aIns):
    for jsonLed in leds:
        led = Led(json.dumps(jsonLed))
        # convert the absolut led position to block relative
        # In which edge is the led
        for edgeIndex in range(1, arena.edges + 1):
            lastLedInEdge = arena.blocks * arena.leds * edgeIndex
            print("last led in edge %d, edge index %d" %
                  (lastLedInEdge, edgeIndex))
            if led.index <= lastLedInEdge:
                print("led in Edge: " + str(edgeIndex))
                # In which block is the led
                for blockIndex in range(-1, (arena.blocks - 1)):
                    blockAbsPos = arena.blocks * edgeIndex + blockIndex
                    print("Block index: %d" % (blockAbsPos))
                    if led.index <= (blockAbsPos * arena.leds):
                        # In which block position is the led
                        ledBlockRelPos = led.index % arena.leds
                        if ledBlockRelPos == 0:
                            ledBlockRelPos = arena.leds
                            break
                        break
                break
        print("LED: %s, %d" % (led.color, led.index))
        bIns = BlockInstruction()
        bIns.brightness = arena.brightness
        bIns.block = \
            str(blockAbsPos - 1) + "," \
            + str(arena.leds) + "," \
            + Color['OMIT'].value
        bIns.led.append(
            str(ledBlockRelPos - 1) + "," + Color[led.color.upper()].value
        )
        # print(bIns.toJSON())
        aIns.send_instrunction(str(bIns.toJSON()))


def edgeBlockToBlock(edIdx, bckPerEd, bckIdx):
    return (edIdx * bckPerEd) - ((bckPerEd - bckIdx) % bckPerEd)


if __name__ == "__main__":
    data = json.loads(JSON_TEST)
    jsonArena = json.dumps(data['arena'])
    jsonBlocks = data['arena']['block']
    jsonEdges = data['arena']['edge']
    jsonLeds = data['arena']['led']
    arena = Arena(jsonArena)
    generateArdInsForArena(arena)
