"""Submit a claim to RocketRide; all research and inference execute on RocketRide."""
import argparse, asyncio, json, re, uuid
from pathlib import Path
from dotenv import dotenv_values
from rocketride import RocketRideClient
from rocketride.schema import Question

ROOT=Path(__file__).resolve().parent

def load_pipeline(config):
    raw=(ROOT/'research.pipe').read_text()
    required=set(re.findall(r'\$\{([A-Z0-9_]+)\}', raw))
    missing=sorted(k for k in required if not config.get(k))
    if missing:
        raise ValueError('Missing configuration: '+', '.join(missing))
    def resolve(value):
        if isinstance(value,str):
            return re.sub(r'\$\{([A-Z0-9_]+)\}',lambda m:config[m[1]],value)
        if isinstance(value,list):return [resolve(v) for v in value]
        if isinstance(value,dict):return {k:resolve(v) for k,v in value.items()}
        return value
    return resolve(json.loads(raw))

async def main(args):
    config=dotenv_values(ROOT/'.env')
    pipeline=load_pipeline(config)
    async with RocketRideClient(uri=config['ROCKETRIDE_URI'],auth=config['ROCKETRIDE_APIKEY']) as client:
        if args.validate:
            print(json.dumps(await client.validate(pipeline),indent=2)); return
        result=await client.use(pipeline=pipeline,ttl=120,pipelineTraceLevel='summary')
        token=result['token']
        try:
            question=Question(); question.addQuestion(args.claim)
            response=await client.chat(token=token,question=question)
            # Never persist any echoed credential, including provider error text.
            raw=json.dumps(response,indent=2)
            for name,value in config.items():
                if value and any(s in name for s in ('KEY','TOKEN','SECRET')):
                    raw=raw.replace(value,'[REDACTED]')
            target=ROOT/'runs'/uuid.uuid4().hex; target.mkdir(parents=True)
            (target/'response.json').write_text(raw)
            print('RocketRide response saved:',target/'response.json')
        finally:
            await client.terminate(token)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('claim',nargs='?',default='Humans can only absorb 30 grams of protein per meal.')
    parser.add_argument('--validate',action='store_true')
    args=parser.parse_args()
    try: asyncio.run(main(args))
    except ValueError as error: parser.exit(2,str(error)+'\n')
