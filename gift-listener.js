const { WebcastPushConnection } = require('tiktok-live-connector');
const WebSocket = require('ws');

// Replace this with your TikTok username (no @)
const tiktokUsername = "your_username";

// Set up WebSocket server
const wss = new WebSocket.Server({ port: 8080 });

// Broadcast function to send commands to Python
function broadcast(data) {
    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify(data));
        }
    });
}

// Set up TikTok connection
let tiktok = new WebcastPushConnection(tiktokUsername);

// Define gift-action map
const giftToCommand = {
    "Rose": "forward",
    "Finger Heart": "left",
    "Perfume": "right",
    "Galaxy": "spin",
    "Treasure Box": "backward"
};

// Handle gift events
tiktok.on('gift', data => {
    const giftName = data.giftName;
    const user = data.uniqueId;

    if (giftToCommand[giftName]) {
        console.log(`${user} sent ${giftName} — triggering ${giftToCommand[giftName]}`);
        broadcast({ command: giftToCommand[giftName] });
    }
});

tiktok.connect().then(() => {
    console.log("Connected to TikTok live as", tiktokUsername);
}).catch(console.error);
