from aiohttp import web


def get_flow_handler(request):
    uuid = request.match_info['uuid']
    response = {
        'uuid': uuid
    }
    return web.json_response(response)
