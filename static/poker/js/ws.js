const tableId = JSON.parse(document.getElementById('table_id').textContent);
const username = JSON.parse(document.getElementById('username').textContent);
const tableSocket = new WebSocket(`ws://${window.location.host}/ws/table/${tableId}/`);

var seats = []
tableSocket.onmessage = function(e) {
    const djangoData = JSON.parse(e.data);
    console.log(djangoData)
    if (djangoData.type === 'seats_arrangement') {
        seats = djangoData.seats;
        console.log(seats)
    } else if (djangoData.type === 'player_info') {
        console.log(seats)
        const i = seats.indexOf(djangoData.username) + 1;
        // image
        const imgElement = document.getElementById(`seat${i}-img`);  
        imgElement.src = `${djangoData.image}`;   
        // username
        document.querySelector(`#seat${i}-username`).innerText = djangoData.username
        // stack
        document.querySelector(`#seat${i}-stack`).innerText = djangoData.stack
    } else if (djangoData.type === 'join') {
        tableSocket.send(JSON.stringify(djangoData));
    }
}

function handleClick(action) {
    tableSocket.send(JSON.stringify({
        'action': action,
        'username': username,
    }));
}

