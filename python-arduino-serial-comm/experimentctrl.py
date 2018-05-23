import json
import copy
import logging

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
    """
    This function executes the arena configuration and its Edge, Block and lEDs
    instructions.
    ----------
    arena : Object
        The arena object which contains the color configuration.

    Returns
    -------

    """
    logging.info(
        "Arena: %d, %d, %d, %s"
        % (arena.edges, arena.blocks, arena.leds, arena.color)
    )
    aIns = ArduinoInstruction('COM5', 57600)
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
    if hasattr(arena, 'edge'):
        rangeOrSingleEdge(arena.edge, arena, aIns, True)
    # Blocks in arena Indvidually
    if hasattr(arena, 'block'):
        rangeOrSingleBlock(arena.block, arena, aIns, True)
    # Leds in arena Indvidually
    if hasattr(arena, 'led'):
        rangeOrSingleLed(arena.led, arena, aIns, True)

    aIns.close_connection()


def generateArdInsForEdge(edge, arena, aIns):
    """
    This function executes the Edge configration and its Block and lEDs
    instructions.
    ----------
    edge : Object
        The edge object which contains the color configuration.

    arena : Object
        The arena object which contains the general configuration.

    aIns : Object
        The serial connection to send the instructions to Arduino.

    Returns
    -------

    """
    # Converting from negative to equivalent positive
    edgeIndex = edge.index[0]
    edgeIndex = \
        fromNegToPosEq(arena.edges, edgeIndex) \
        if (edgeIndex < 0) else edgeIndex
    logging.info("Edge: %s, %d" % (edge.color, edgeIndex))
    for i in range(-1, (arena.blocks - 1)):
        bIns = BlockInstruction()
        bIns.brightness = arena.brightness
        bIns.block = \
            str((edgeIndex * arena.blocks + i) - 1) + "," \
            + str(arena.leds) + "," \
            + Color[edge.color.upper()].value
        aIns.send_instrunction(str(bIns.toJSON()))
    # If there are some blocks, execute them.
    if hasattr(edge, 'block'):
        for jsonBlock in edge.block:
            space = arena.edges * arena.blocks
            jsonBlock['index'] = rangeToList(jsonBlock['index'])
            newBlockRange = []
            for rBlock in jsonBlock['index']:
                newBlockRange.append(
                    fromRelPosToAbsPos(
                        # -1 means last index
                        edgeIndex, arena.blocks, rBlock, space
                    )
                )
            jsonBlock['index'] = newBlockRange
        rangeOrSingleBlock(edge.block, arena, aIns, False)
    # If there are some leds, execute them.
    if hasattr(edge, 'led'):
        for jsonLed in edge.led:
            ledsPerEdge = arena.blocks * arena.leds
            space = arena.edges * arena.blocks * arena.leds
            jsonLed['index'] = rangeToList(jsonLed['index'])
            newLedRange = []
            for rled in jsonLed['index']:
                newLedRange.append(
                    fromRelPosToAbsPos(edgeIndex, ledsPerEdge, rled, space)
                )
            jsonLed['index'] = newLedRange
        rangeOrSingleLed(edge.led, arena, aIns, False)


def generateArdInsForBlock(block, arena, aIns):
    """
    This function executes the Block configuration and its lEDs instructions.
    ----------
    block : Object
        The block object which contains the color configuration.

    arena : Object
        The arena object which contains the general configuration.

    aIns : Object
        The serial connection to send the instructions to Arduino.

    Returns
    -------

    """
    ledsOutOfRange = []
    blockIndex = block.index[0]
    # Converting from negative to equivalent positive
    blockIndex = \
        fromNegToPosEq(arena.blocks * arena.edges, blockIndex)\
        if (blockIndex < 0) else blockIndex
    #
    logging.info("Block: %s, %d" % (block.color, blockIndex))
    bIns = BlockInstruction()
    bIns.brightness = arena.brightness
    bIns.block = \
        str(blockIndex - 1) + "," \
        + str(arena.leds) + "," \
        + Color[block.color.upper()].value
    # If there are some leds, add them to the block instruction. # si algo sale mal segurament es aqui
    if hasattr(block, 'led'):
        for jsonLed in block.led:
            led = Led(json.dumps(jsonLed))
            led.index = rangeToList(led.index)
            if len(led.index) > 1:
                lRange = led.index
                for index in lRange:
                    if index != 0:
                        tmpLed = copy.copy(led)
                        tmpLed.index = [index]
                        if not (tmpLed.index[0] < 0 or tmpLed.index[0] > arena.leds):
                            bIns.led.append(
                                str(tmpLed.index[0] - 1) + "," +
                                Color[led.color.upper()].value
                            )
                        else:  # This is for the leds out of range
                            space = arena.edges * arena.blocks * arena.leds
                            orIndex = fromRelPosToAbsPos(  # outOfRangIndex
                                blockIndex, arena.leds, tmpLed.index[0], space
                            )
                            ledsOutOfRange.append(
                                {'index': [orIndex], 'color': led.color}
                            )
            else:
                if not (led.index[0] < 0 or led.index[0] > arena.leds):
                    bIns.led.append(
                        str(led.index[0] - 1) + "," +
                        Color[led.color.upper()].value
                    )
                else:  # This is for the leds out of range
                    space = arena.edges * arena.blocks * arena.leds
                    orIndex = fromRelPosToAbsPos(  # outOfRangIndex
                        blockIndex, arena.leds, led.index[0], space
                    )
                    ledsOutOfRange.append(
                        {'index': [orIndex], 'color': led.color}
                    )
    logging.info(bIns.toJSON())
    aIns.send_instrunction(str(bIns.toJSON()))
    rangeOrSingleLed(ledsOutOfRange, arena, aIns, False)


def generateArdInsForLed(led, arena, aIns):
    """
    This function executes the LEDs configuration.
    ----------
    Led : Object
        The Led object which contains the color configuration.

    arena : Object
        The arena object which contains the general configuration.

    aIns : Object
        The serial connection to send the instructions to Arduino.

    Returns
    -------

    """
    ledIndex = led.index[0]
    if ledIndex < 0:
        ledIndex = fromNegToPosEq(
            arena.edges * arena.blocks * arena.leds, ledIndex
        )
    # convert the absolut led position to block relative
    # In which edge is the led
    for edgeIndex in range(1, arena.edges + 1):
        lastLedInEdge = arena.blocks * arena.leds * edgeIndex
        logging.info(
            "last led in edge %d, edge index %d" % (lastLedInEdge, edgeIndex)
        )
        if ledIndex <= lastLedInEdge:
            logging.info("led in Edge: %d" % (edgeIndex))
            # In which block is the led
            for blockIndex in range(-1, (arena.blocks - 1)):
                blockAbsPos = arena.blocks * edgeIndex + blockIndex
                logging.info("Block index: %d" % (blockAbsPos))
                if ledIndex <= (blockAbsPos * arena.leds):
                    # In which block position is the led
                    ledBlockRelPos = ledIndex % arena.leds
                    if ledBlockRelPos == 0:
                        ledBlockRelPos = arena.leds
                        break
                    break
            break
    logging.info("LED: %s, %d" % (led.color, ledIndex))
    bIns = BlockInstruction()
    bIns.brightness = arena.brightness
    bIns.block = \
        str(blockAbsPos - 1) + "," \
        + str(arena.leds) + "," \
        + Color['OMIT'].value
    bIns.led.append(
        str(ledBlockRelPos - 1) + "," + Color[led.color.upper()].value
    )
    logging.info(bIns.toJSON())
    aIns.send_instrunction(str(bIns.toJSON()))


def fromRelPosToAbsPos(edIdx, bckPerEd, bckIdx, space):  # edgeBlock->Block
    """
    This function transform the relative position of an index using the 
    relative index, the number of blocks per edge, the index block and the space
    in which this index should be. The function accepts negative indexes.
    ----------
    edIdx : Object
        Index of edge in which the idnex to transform is.

    bckPerEd : Object
        Number of blocks that form an edge.

    bckIdx : Object
        Index to transform.

    space : Object
        The space within the index should be.

    Returns
    -------

    """
    if bckPerEd == 1:
        return bckIdx
    elif bckIdx < 0:
        return (((edIdx * bckPerEd) - ((bckPerEd - bckIdx))) % space) + 1
    else:
        newIndex = ((edIdx * bckPerEd) - ((bckPerEd - bckIdx))) % space
        return newIndex if (newIndex > 0) else space


def fromNegToPosEq(space, number):
    """
    This function transform a negative number to its positive equivalent.
    ----------
    numnber : Object
        The negative number to transform.

    space : Object
        The space within the index should be.

    Returns
    -------

    """
    if space == 1:
        return abs(number)
    else:
        return (number % space) + 1


def rangeOrSingleEdge(edges, arena, aIns, fromArena):
    """
    This function execute a range of Edges or a single Edge.
    ----------
    edges : Object
        An array of edges which lenght can be 0, 1 or more.

    arena : Object
        The arena object which contains the general configuration.

    aIns : Object
        The serial connection to send the instructions to Arduino.

    fromArena : Boolean
        Specify if the range or single edge comes from the arena enviroment.

    Returns
    -------

    """
    for jsonEdge in edges:
        edge = Edge(json.dumps(jsonEdge))
        if len(edge.index) > 1:
            eRange = rangeToList(edge.index) \
                if(fromArena)else edge.index
            for index in eRange:  # to-do change to reverse order reversed()
                index = fromRelPosToAbsPos(
                    index, arena.edges, index, arena.edges
                )
                if index != 0:
                    tmpEdge = copy.copy(edge)
                    tmpEdge.index = [index]
                    # to-do change from last to first
                    if not(index == eRange[-1]):
                        tmpEdge.block = []
                        tmpEdge.led = []
                        generateArdInsForEdge(tmpEdge, arena, aIns)
                    else:
                        generateArdInsForEdge(tmpEdge, arena, aIns)

        else:
            generateArdInsForEdge(edge, arena, aIns)


def rangeOrSingleBlock(blocks, arena, aIns, fromArena):
    """
    This function execute a range of Blocks or a single one.
    ----------
    blocks : Object
        An array of blocks which lenght can be 0, 1 or more.

    arena : Object
        The arena object which contains the general configuration.

    aIns : Object
        The serial connection to send the instructions to Arduino.

    fromArena : Boolean
        Specify if the range or single edge comes from the arena enviroment.

    Returns
    -------

    """
    for jsonBlock in blocks:
        block = Block(json.dumps(jsonBlock))
        if len(block.index) > 1:
            bRange = rangeToList(block.index) if (fromArena) else block.index
            for index in bRange:  # to-do change to reverse order reversed()
                if index != 0:
                    tmpBlock = copy.copy(block)
                    tmpBlock.index = [index]
                    # to-do change from last to first
                    if not(index == bRange[-1]):
                        tmpBlock.led = []
                        generateArdInsForBlock(tmpBlock, arena, aIns)
                    else:
                        generateArdInsForBlock(tmpBlock, arena, aIns)
        else:
            generateArdInsForBlock(block, arena, aIns)


def rangeOrSingleLed(leds, arena, aIns, fromArena):
    """
    This function execute a range of Leds instructions or a single one.
    ----------
    Leds : Object
        An array of leds which lenght can be 0, 1 or more.

    arena : Object
        The arena object which contains the general configuration.

    aIns : Object
        The serial connection to send the instructions to Arduino.

    fromArena : Boolean
        Specify if the range or single edge comes from the arena enviroment.

    Returns
    -------

    """
    for jsonLed in leds:
        led = Led(json.dumps(jsonLed))
        if len(led.index) > 1:
            lRange = rangeToList(led.index)\
                if (fromArena) else led.index
            for index in lRange:
                if index != 0:
                    tmpLed = copy.copy(led)
                    tmpLed.index = [index]
                    generateArdInsForLed(tmpLed, arena, aIns)
        else:
            generateArdInsForLed(led, arena, aIns)


def rangeToList(rng):
    """
    This function transform a python range to a list of values.
    ----------
    range : Object
        A python range.

    Returns
    -------
    List which contains the respective range values.

    """
    list = []
    if len(rng) == 3:
        list = range(rng[0], rng[1] - 1, rng[2]) \
            if (rng[0] > rng[1]) else range(rng[0], rng[1] + 1, rng[2])
        return list
    elif len(rng) == 2:
        list = range(rng[0], rng[1] - 1)\
            if (rng[0] > rng[1]) else range(rng[0], rng[1] + 1)
        return list
    elif len(rng) == 1:
        return rng
