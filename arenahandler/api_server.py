from aiohttp import web
import asyncio
import json
import sched
import time
import argparse

import experiment.experimentctrl as ec


async def runExperiment(request):
    data = await request.json()
    asyncio.ensure_future(ec.runExperiment(data))
    response_obj = {'status': 'received'}
    return web.Response(text=json.dumps(response_obj))


async def runState(request):
    data = await request.json()
    asyncio.ensure_future(ec.runState(data))
    response_obj = {'status': 'received'}
    return web.Response(text=json.dumps(response_obj))


def main():

    parser = argparse.ArgumentParser(description='ArenaHandler API Server')
    parser.add_argument(
        '--port', type=int, help='http listening port, default: 8080'
    )
    args = parser.parse_args()
    app = web.Application()
    app.router.add_post('/arena-handler/api/v1.0/experiment', runExperiment)
    app.router.add_post('/arena-handler/api/v1.0/state', runState)
    web.run_app(app, host="localhost", port=args.port)


if __name__ == '__main__':
    main()
