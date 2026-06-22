import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# Initialize the backend application
app = FastAPI(title="Intelligent SCADA Backend")

# Security policy to allow your HTML file to communicate with this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connection Manager to handle the ESP32 and Dashboard(s)
class ConnectionManager:
    def __init__(self):
        # Keeps a list of everything connected to the server
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"[+] Device Connected! Total active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"[-] Device Disconnected. Total active connections: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        # Fires the incoming data out to every connected screen instantly
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                pass

manager = ConnectionManager()

# This is the dedicated pipeline for real-time IoT data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # 1. Server waits to receive a JSON string
            data = await websocket.receive_text()
            
            # 2. Print it to the VS Code terminal so you can verify it's working
            print(f"Incoming Telemetry: {data}")
            
            # 3. Instantly push that data to the HTML dashboard
            await manager.broadcast(data)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    print("🚀 Starting SCADA Predictive Maintenance Backend...")
    print("📡 WebSocket listening on ws://localhost:8000/ws")
    # Run the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)