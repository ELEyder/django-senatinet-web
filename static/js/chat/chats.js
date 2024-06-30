import { db } from '../firebaseConfig.js';
import { loadMessages } from './messages.js';

const dominioBase = window.location.origin;

// Changes Realtime
db.collection('chats').onSnapshot(snapshot => {
    // Llamar a la función loadChats dentro de la función de callback
    loadChats()
    .then(() => {
        snapshot.docChanges().forEach(change => {
            if (change.type === 'added') {
                var idchat = change.doc.id;
                var element = document.querySelector(`[idChat="${idchat}"]`);
                if (element) {
                    element.click();
                }
                closeOverlay();
            }
        });
    })
    .catch(error => {
        console.error('Error al cargar los chats y procesar cambios:', error);
    });
});

function loadChats(){
    return fetch(`${dominioBase}/chat/get`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        var chatsBody = document.getElementById('chats-body')
        chatsBody.innerHTML = ''
        data.chats.forEach(chat => {
            var chatHtml = `
            <div id="loadMessages" idChat="${chat.id}" fullName="${chat.receiverFirstName} ${chat.receiverLastName}" receiverId="${chat.receiver}" receiverStatus="${chat.receiverStatus}" class="btn-chat loadMessages">
                <div class="default-user-state">
                    <div class="avatar-icon">
                        <img src="${chat.receiverUrlAvatar}" alt="avatar" class="avatar-icon">
                    </div>
                    <div class="state default-user">
                        <div class="state-circle default-user ${chat.receiverStatus}"></div>
                    </div> 
                </div>
                <div>
                    <p>${chat.receiverFirstName} ${chat.receiverLastName}</p>`
                    if (chat.lastMessage != undefined) {
                        chatHtml += `<p>${chat.lastMessage}</p>`
                    }
                `</div> 
            </div>
            `;
            chatsBody.innerHTML += chatHtml;
        });
        console.log('Respuesta del servidor:', data);
        // Add event load messages from chat
        let buttons = document.querySelectorAll('.loadMessages');
        buttons.forEach(button => {
            button.addEventListener('click', loadMessages);
        })
    })
    .catch(error => {
        console.error('Error al enviar el mensaje:', error);
    });
}

export function addChat(event){
    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    const button = event.currentTarget;
    const id = button.getAttribute('idFriend');
    const messageData = {
        friend: id,
    };

    fetch(`${dominioBase}/chat/add/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(messageData),
    })
    .then(response => response.json())
    .then(data => {
        closeOverlay()
        console.log('Respuesta del servidor:', data);
        if (!data.response) {
            var idchat = data.idchat;
            var element = document.querySelector(`[idChat="${idchat}"]`);
            if (element) {
                element.click();
            }
        }
    })
    .catch(error => {
        console.error('Error al añadir el chat:', error);
    });
}

const friendsButtons = document.querySelectorAll('.friend-chat');
friendsButtons.forEach(button => {
    button.addEventListener('click', addChat);
});