import json
import copy

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
    # print(
    #    "Arena: %d, %d, %d, %s"
    #    % (arena.edges, arena.blocks, arena.leds, arena.color)
    #)
    aIns = ArduinoInstruction('COM4', 57600)
    aIns.start_connection()
    for i in range(0, (arena.blocks * arena.edges)):
        bIns = BlockInstruction()
        bIns.brightness = arena.brightness
        bIns.block = \
            str(i) + "," \
            + str(arena.leds) + "," \
            + Color[arena.color.upper()].value
        print(aIns.send_instrunction(str(bIns.toJSON())))
    # Edges in arena Individually
    rangeOrSingleEdge(arena.edge, arena, aIns)
    # Blocks in arena Indvidually
    rangeOrSingleBlock(arena.block, arena, aIns)
    # Leds in arena Indvidually
    generateArdInsForLed(arena.led, arena, aIns)
    aIns.close_connection()


def generateArdInsForEdge(edge, arena, aIns):
    # Converting from negative to equivalent positive
    edgeIndex = edge.index[0]
    edgeIndex = \
        fromNegToPosEq(arena.edges, edgeIndex) \
        if (edgeIndex < 0) else edgeIndex
    # print("Edge: %s, %d, %a" % (edge.color, edgeIndex, edge.block))
    for i in range(-1, (arena.blocks - 1)):
        bIns = BlockInstruction()
        bIns.brightness = 25
        bIns.block = \
            str((edgeIndex * arena.blocks + i) - 1) + "," \
            + str(arena.leds) + "," \
            + Color[edge.color.upper()].value
        aIns.send_instrunction(str(bIns.toJSON()))
    # If there are some blocks, execute them.
    for jsonBlock in edge.block:
        space = arena.edges * arena.blocks
        jsonBlock['index'] = [
            fromRelPosToAbsPos(
                edgeIndex, arena.blocks, jsonBlock['index'][-1], space # -1 means last index
            )
        ]
    rangeOrSingleBlock(edge.block, arena, aIns)
    # If there are some leds, execute them.
    for jsonLed in edge.led:
        ledsPerEdge = arena.blocks * arena.leds
        space = arena.edges * arena.blocks * arena.leds
        jsonLed['index'] = \
            fromRelPosToAbsPos(
                edgeIndex, ledsPerEdge, jsonLed['index'], space
        )
    generateArdInsForLed(edge.led, arena, aIns)


def generateArdInsForBlock(block, arena, aIns):
    ledsOutOfRange = []
    blockIndex = block.index[0]
    # Converting from negative to equivalent positive
    blockIndex = \
        fromNegToPosEq(arena.blocks * arena.edges, blockIndex)\
        if (blockIndex < 0) else blockIndex
    #
    # print("Block: %s, %d, %a" % (block.color, blockIndex, block.led))
    bIns = BlockInstruction()
    bIns.brightness = arena.brightness
    bIns.block = \
        str(blockIndex - 1) + "," \
        + str(arena.leds) + "," \
        + Color[block.color.upper()].value
    # If there are some leds, add them to the block instruction.
    for jsonLed in block.led:
        led = Led(json.dumps(jsonLed))
        if not (led.index < 0 or led.index > arena.leds):
            bIns.led.append(
                str(led.index - 1) + "," + Color[led.color.upper()].value
            )
        else:  # This is for the leds out of range
            space = arena.edges * arena.blocks * arena.leds
            index = fromRelPosToAbsPos(
                blockIndex, arena.leds, led.index, space
            )
            ledsOutOfRange.append({'index': index, 'color': led.color})
    # print(bIns.toJSON())
    aIns.send_instrunction(str(bIns.toJSON()))
    generateArdInsForLed(ledsOutOfRange, arena, aIns)


def generateArdInsForLed(leds, arena, aIns):
    for jsonLed in leds:
        led = Led(json.dumps(jsonLed))
        # convert the absolut led position to block relative
        # In which edge is the led
        for edgeIndex in range(1, arena.edges + 1):
            lastLedInEdge = arena.blocks * arena.leds * edgeIndex
            # print("last led in edge %d, edge index %d" %
            #       (lastLedInEdge, edgeIndex))
            if led.index <= lastLedInEdge:
                # print("led in Edge: " + str(edgeIndex))
                # In which block is the led
                for blockIndex in range(-1, (arena.blocks - 1)):
                    blockAbsPos = arena.blocks * edgeIndex + blockIndex
                    # print("Block index: %d" % (blockAbsPos))
                    if led.index <= (blockAbsPos * arena.leds):
                        # In which block position is the led
                        ledBlockRelPos = led.index % arena.leds
                        if ledBlockRelPos == 0:
                            ledBlockRelPos = arena.leds
                            break
                        break
                break
        # print("LED: %s, %d" % (led.color, led.index))
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


def fromRelPosToAbsPos(edIdx, bckPerEd, bckIdx, space):  # edgeBlock->Block
    if bckPerEd == 1:
        return bckIdx
    elif bckIdx < 0:
        return (((edIdx * bckPerEd) - ((bckPerEd - bckIdx))) % space) + 1
    else:
        newIndex = ((edIdx * bckPerEd) - ((bckPerEd - bckIdx))) % space
        return newIndex if (newIndex > 0) else space


def fromNegToPosEq(space, number):
    if space == 1:
        return abs(number)
    else:
        return (number % space) + 1


def listToRange(list):
    if len(list) == 1:
        return list[0]
    elif len(list) == 2:
        return range(list[0], list[1])
    elif len(list) == 3:
        return range(list[0], list[1], list[2])


def rangeOrSingleEdge(edges, arena, aIns):
    for jsonEdge in edges:
        edge = Edge(json.dumps(jsonEdge))
        if len(edge.index) > 1:
            eRange = listToRange(edge.index)
            for index in eRange:
                if index != 0:
                    tmpEdge = copy.copy(edge)
                    tmpEdge.index = [index]
                    generateArdInsForEdge(tmpEdge, arena, aIns)
        else:
            generateArdInsForEdge(edge, arena, aIns)


def rangeOrSingleBlock(blocks, arena, aIns):
    for jsonBlock in blocks:
        block = Block(json.dumps(jsonBlock))
        if len(block.index) > 1:
            bRange = listToRange(block.index)
            for index in bRange:
                if index != 0:
                    tmpBlock = copy.copy(block)
                    tmpBlock.index = [index]
                    generateArdInsForBlock(tmpBlock, arena, aIns)
        else:
            generateArdInsForBlock(block, arena, aIns)


def rangeOrSingleLed():
    pass
