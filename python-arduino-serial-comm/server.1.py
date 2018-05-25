from aiohttp import web
import asyncio
import json
import sched
import time

import experimentctrl as ec

async def runExperiment(request):
    data = await request.json()
    asyncio.ensure_future(ec.runExperiment(data))
    response_obj = { 'status' : 'received' }
    return web.Response(text=json.dumps(response_obj))

async def runState(request):
    data =  await request.json()
    asyncio.ensure_future(ec.runState(data))
    response_obj = { 'status' : 'received' }
    return web.Response(text=json.dumps(response_obj))

app = web.Application()
app.router.add_post('/arena-handler/api/v1.0/experiment', runExperiment)
app.router.add_post('/arena-handler/api/v1.0/state', runState)
web.run_app(app)
