import json

from ArduinoInstruction import ArduinoInstruction
from Arena import Arena
from Edge import Edge
from Block import Block
from Led import Led
from BlockInstruction import BlockInstruction
from Color import Color


def runState(state):
    jsonArena = json.dumps(state['arena'])
    arena = Arena(jsonArena)
    generateArdInsForArena(arena)


def runExperiment(experiment):
    pass


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
    # Edges in arena Individually
    generateArdInsForEdge(arena.edge, arena, aIns)
    # Blocks in arena Indvidually
    generateArdInsForBlock(arena.block, arena, aIns)
    # Leds in arena Indvidually
    generateArdInsForLed(arena.led, arena, aIns)
    aIns.close_connection()


def generateArdInsForEdge(edges, arena, aIns):

    for jsonEdge in edges:
        edge = Edge(json.dumps(jsonEdge))
        # Converting from negative to equivalent positive
        edge.index = \
            fromNegToPosEq(arena.edges, edge.index) \
            if (edge.index < 0) else edge.index
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
                fromRelPosToAbsPos(edge.index, arena.blocks,
                                   jsonBlock['index'])
        generateArdInsForBlock(edge.block, arena, aIns)
        # If there are some leds, execute them.
        for jsonLed in edge.led:
            jsonLed['index'] = \
                fromRelPosToAbsPos(
                    edge.index, (arena.blocks *
                                 arena.leds), jsonLed['index']
            )
        generateArdInsForLed(edge.led, arena, aIns)


def generateArdInsForBlock(blocks, arena, aIns):
    for jsonBlock in blocks:
        block = Block(json.dumps(jsonBlock))
        # Converting from negative to equivalent positive
        block.index = \
            fromNegToPosEq(arena.blocks * arena.edges, block.index)\
            if (block.index < 0) else block.index
        #
        print("Block: %s, %d, %a" % (block.color, block.index, block.led))
        bIns = BlockInstruction()
        bIns.brightness = arena.brightness
        bIns.block = \
            str(block.index - 1) + "," \
            + str(arena.leds) + "," \
            + Color[block.color.upper()].value
        # If there are some leds, add them to the block instruction.
        for jsonLed in block.led:
            led = Led(json.dumps(jsonLed))
            # Converting from negative to equivalent positive
            led.index = \
                fromNegToPosEq(arena.blocks * arena.edges * arena.leds, led.index)\
                if (led.index < 0) else led.index
            #
            led.index = \
                fromRelPosToAbsPos(
                    block.index, arena.leds, led.index
                )
            print(led.index)
            bIns.led.append(
                str(led.index - 1) + "," + Color[led.color.upper()].value
            )
        # print(bIns.toJSON())
        aIns.send_instrunction(str(bIns.toJSON()))


def generateArdInsForLed(leds, arena, aIns):
    for jsonLed in leds:
        led = Led(json.dumps(jsonLed))
        # Converting from negative to equivalent positive
        led.index = \
            fromNegToPosEq(arena.blocks * arena.edges * arena.leds, led.index)\
            if (led.index < 0) else led.index
        #
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
        print(bIns.toJSON())
        aIns.send_instrunction(str(bIns.toJSON()))


def fromRelPosToAbsPos(edIdx, bckPerEd, bckIdx):  # edgeBlock->Block
    if bckPerEd == 1:
        return bckIdx
    else:
        return (edIdx * bckPerEd) - ((bckPerEd - bckIdx) % bckPerEd)


def fromNegToPosEq(space, number):
    if space == 1:
        return abs(number)
    else:
        return (number % space) + 1
