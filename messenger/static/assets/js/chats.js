const chats = (() => {
    const TOKEN = "Bearer"
    let that = {}
    let currentConnection;

    that.loadChats = () => {
        const currentToken = localStorage.getItem(TOKEN)
        console.log("load chats")

        let myChats = document.getElementById('mychats')
        myChats.innerHTML = ""; //clear before insert

        fetch('/chat/my', {method: 'GET', headers: { Authorization: "Bearer " + currentToken }}).then(r => r.json())
            .then(data => data.forEach(element => {
                let chatItem = createElementFromHTML(`<li>${element.name}</li>`)
                chatItem.onclick = () => that.selectChat(element.id)
                myChats.appendChild(chatItem)
            }))
    }


    that.selectChat = (chatId) => {
        if(!!currentConnection && currentConnection.chatId != chatId && !!currentConnection.socket) {
            currentConnection.socket.close();
        }
        const currentToken = localStorage.getItem(TOKEN)
        let messagesElement = document.getElementById('messages')

        messagesElement.innerHTML = "";

        fetch(`/message/chat?chat_id=${chatId}`, {method: 'GET', headers: { Authorization: "Bearer " + currentToken }})
            .then(response => {
                if(response.ok) {
                    let data = response.json()
                    data.then(d=> Array.from(d))
                        .then((d) => d.forEach(message => {
                            that.displayMessage(message, messagesElement)
                        }));
                }
            });

        let socket = new WebSocket(`ws://127.0.0.1:8000/ws/${chatId}`)

        currentConnection = {
            chatId: chatId,
            socket: socket
        }

        socket.onmessage = (event) => {
            let data = JSON.parse(event.data.replace(/(?:\\[rn])+/g, ''))
            that.displayMessage(JSON.parse(data), messagesElement)
        }

        socket.onopen = () => {
            let status = document.getElementById('ws-status')

            status.innerText = "connected"
            status.style.color = "green"
        }

        socket.onclose = () => {
            let status = document.getElementById('ws-status')

            status.innerText = "disconnected"
            status.style.color = "red"
            currentConnection = null;
        }
    }

    that.displayMessage = (message,container) => {
        let messageElement = createElementFromHTML(`<li>${message.text}</li>`)
        container.appendChild(messageElement)
    }

    that.sendMessage = async () => {
        if(!!currentConnection) {
            let currentUser = await login.getLoggedUser();
            var input = document.getElementById("messageText")
            const json_request_body = JSON.stringify({
                user_id: currentUser.id,
                chat_id: currentConnection.chatId,
                text: input.value,
                edited: false,
                read: false
            });

            fetch(`/message/`, {method: 'POST', headers: { Authorization: "Bearer " + TOKEN, "Content-Type": "application/json" }, body: json_request_body})
            input.value = ''
        }
    }

    return {
        loadChats: async () => {
            if (await login.requestLoginAndPasswordIfNotLoggedIn()) {
                return await that.loadChats()
            }

            return false;
        },
        sendMessage: async () => {
            if (await login.requestLoginAndPasswordIfNotLoggedIn()) {
                return await that.sendMessage()
            }
        },
        
        reconnect: async () => {
            if(!!currentConnection && !!currentConnection.chatId) {
                that.selectChat(currentConnection.chatId);
            }
        }
    }
})()