# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 09:31:32 2023

@author: nisha
"""

import asyncio
from datetime import datetime
import json
import os
import pandas as pd
from pyensign.events import Event
from pyensign.ensign import Ensign
from pathlib import Path
from dotenv import load_dotenv
import websockets

# Global variables
topic = "Finnhub-json"
dotenv_path = Path('./config/.env')
load_dotenv(dotenv_path=dotenv_path)
ClientID = os.environ.get("ClientID")
ClientSecret = os.environ.get("ClientSecret")

ensign = Ensign(client_id=ClientID, client_secret=ClientSecret)
symbols = ["AAPL", "MSFT"]
df = pd.DataFrame(columns=["symbol", "time", "price"])


async def handle_ack(ack):
    _ = datetime.fromtimestamp(ack.committed.seconds + ack.committed.nanos / 1e9)

async def handle_nack(nack):
    print(f"Could not commit event {nack.id} with error {nack.code}: {nack.error}")

async def recv_and_publish(uri):
        """
        Receive messages from the websocket and publish events to Ensign.
        """
        while True:

            try:
                async with websockets.connect(uri) as websocket:
                    for symbol in symbols:
                        await websocket.send(
                            f'{{"type":"subscribe","symbol":"{symbol}"}}'
                        )
                    

                    while True:
                        message = await websocket.recv()
                        for event in message_to_events(json.loads(message)):
                            await ensign.publish(
                                topic, event, on_ack=handle_ack, on_nack=handle_nack
                            )
               
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Websocket connection closed: {e}")
                continue

def message_to_events(message):
        """
        Convert a message from the Finnhub API to an Ensign event.
        """
        message_type = message["type"]
        if message_type == "ping":
            return
        elif message_type == "trade":
            for trade in message["data"]:
                data = {
                    "price": trade["p"],
                    "symbol": trade["s"],
                    "timestamp": trade["t"]
                    #,
                    #"volume": trade["v"],
                }
                yield Event(
                    json.dumps(data).encode("utf-8"), mimetype="application/json"
                )
        else:
            raise ValueError(f"Unknown message type: {message_type}")
       
def get_timestamp(epoch):
    
        """
        converts unix epoch to datetime
        """
        epoch_time = epoch / 1000.0
        timestamp = datetime.fromtimestamp(epoch_time)
          
        
        return timestamp
        
async def subscribe():
    """ 
    Subscribe to topic and populate line chart in a Streamlit app
    """
    async for event in ensign.subscribe(topic):
        global df
        data = json.loads(event.data)
        # convert unix epoch to datetime
        timestamp = get_timestamp(data["timestamp"])
        message = dict()
        message["symbol"] = data["symbol"]
        #message["time"] = timestamp.strftime("%H:%M:%S")
        message["day"] = timestamp.strftime("%x")
        message["HrMin"] = timestamp.strftime("%H:%M")
        message["Second"] = timestamp.strftime("%S")
        message["timestamp"] = timestamp.strftime("%f")
        #message["timestamp"] = timestamp.strftime("%H:%M:%S.%fZ")
        message["price"] = str(data["price"])
        #message["volume"] = str(data["volume"])
        # add new data to dataframe
        print(message)

async def main():
    # Load FINNHUB_API_KEY from environment variable
    token = os.environ.get("finnhub")
    if token is None:
        raise ValueError("finnhub environment variable not set.")

    # Create the subscribe and publish tasks and run them asynchronously
    subscribe_task = asyncio.create_task(subscribe())
    publish_task = asyncio.create_task(recv_and_publish(f"wss://ws.finnhub.io?token={token}&skip=5"))
    await asyncio.gather(subscribe_task, publish_task)

if __name__ == "__main__":
      
     
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
         asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()