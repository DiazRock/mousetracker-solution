const ws = new WebSocket("ws://" + location.host + "/ws");
console.log("Connection done!");

ws.onmessage = function(event) {
    console.log("Having a message");
    const data = JSON.parse(event.data);
    if (data.type === 'move') {
        //console.log("Movement message");
        const movementDiv = document.getElementById('movementEvent');
        movementDiv.innerHTML = 'Mouse moved to (' + data.x + ', ' + data.y + ')';
        ws.send(JSON.stringify({ x: data.x, y: data.y, event:'mousemove' }));
    } else if (data.type === 'click') {
        console.log("Click message");
        const clickEvent = document.getElementById('clickEvent');
        const action = data.pressed ? 'pressed' : 'released';
        clickEvent.innerHTML = 'Mouse ' + data.button + ' ' + action + ' at (' + data.x + ', ' + data.y + ')';
        console.log('Sending data via the websocket connection');
        ws.send(JSON.stringify({ x: data.x, y: data.y, event: 'lclick', action: action }));
    }
};