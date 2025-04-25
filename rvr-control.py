import asyncio
import websockets
import json
from sphero_sdk import SerialAsyncDal
from sphero_sdk import SpheroRvrObserver

# Connect to Sphero RVR
dal = SerialAsyncDal()
rvr = SpheroRvrObserver(dal=dal)

async def main():
    await dal.initialize()
    await rvr.wake()

    async def handle_command(websocket, _):
        async for message in websocket:
            data = json.loads(message)
            command = data.get("command", "")
            print(f"Received command: {command}")

            if command == "forward":
                rvr.drive_with_heading(speed=64, heading=0, flags=0)
            elif command == "backward":
                rvr.drive_with_heading(speed=64, heading=180, flags=0)
            elif command == "left":
                rvr.drive_with_heading(speed=64, heading=270, flags=0)
            elif command == "right":
                rvr.drive_with_heading(speed=64, heading=90, flags=0)
            elif command == "spin":
                await rvr.raw_motors(
                    left_mode=2, left_duty_cycle=64,
                    right_mode=1, right_duty_cycle=64
                )
            await asyncio.sleep(5)
            await rvr.drive_with_heading(speed=0, heading=0, flags=0)

    async with websockets.serve(handle_command, "localhost", 8080):
        await asyncio.Future()  # run forever

asyncio.run(main())
