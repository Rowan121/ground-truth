"""Read-only provider checks. Run with .venv/bin/python check_connections.py."""
import asyncio
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from dotenv import dotenv_values
from rocketride import RocketRideClient

config = dotenv_values('.env')

def check_http(name, url, headers):
    try:
        with urlopen(Request(url, headers=headers), timeout=20) as response:
            json.load(response)
            print(f'{name}: connected (HTTP {response.status})')
    except HTTPError as error:
        print(f'{name}: HTTP {error.code}')
    except Exception as error:
        print(f'{name}: {type(error).__name__}')

async def main():
    check_http('Cognee', config['COGNEE_BASE_URL'] + '/api/v1/datasets/',
               {'X-Api-Key': config['COGNEE_API_KEY']})
    check_http('Hotdata', 'https://api.hotdata.dev/v1/workspaces',
               {'Authorization': 'Bearer ' + config['HOTDATA_API_TOKEN']})
    client = RocketRideClient(uri=config.get('ROCKETRIDE_URI', 'https://staging.rocketride.ai'),
                              auth=config['ROCKETRIDE_APIKEY'])
    try:
        await client.connect(timeout=20000)
        print('RocketRide: authenticated')
    except Exception as error:
        print(f'RocketRide: {type(error).__name__}')
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
