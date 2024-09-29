console.log('js loaded');

const ws = new WebSocket('ws://127.0.0.1:5000');

const formChat = document.getElementById('message-send');
const usernameField = formChat.querySelector('input[name="username"]');
const messageField = formChat.querySelector('textarea[name="message"]');
const subscribe = document.getElementById('messages'); 

formChat.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const messageData = {
        username: usernameField.value,
        message: messageField.value
    };

    console.log(messageData);

    ws.send(JSON.stringify(messageData));

    messageField.value = '';
});

ws.onopen = (e) => {
    console.log('Connected to WebSocket server!');
};

ws.onmessage = (e) => {
    console.log(e.data);
    
    const data = JSON.parse(e.data);
    const text = `${data.username}: ${data.message}`; 

    const elMsg = document.createElement('div');
    elMsg.textContent = text;

    subscribe.appendChild(elMsg);
};

