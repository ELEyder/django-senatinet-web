import { db } from '../firebaseConfig.js';

const dominioBase = window.location.origin;

const idUser = document.querySelector('[name="idUser"]').value;

db.collection(`chats`).where('members', 'array-contains',  idUser).onSnapshot(snapshot => {
    snapshot.forEach(doc => {
        console.log(doc.id, " => ", doc.data());
    });
    alert('cambio el chat')
    loadMessages();
});

export function loadMessages(event){
    const button = event.currentTarget;
    var id = button.getAttribute('idchat')
    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    const body = {
        id : id,
    };
    fetch(`${dominioBase}/chat/get/messages/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(body),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const messagesDiv = document.getElementById('chat-details');
        const header = document.getElementById('chat-header');
        
        var avatarUrl = button.getElementsByTagName('img')[0].getAttribute('src')
        var receiverStatus = button.getAttribute('receiverStatus')
        var fullName = button.getAttribute('fullname')
        var receiverId = button.getAttribute('receiverId')

        var input = document.getElementById('input-chat')
        // HEADER CHAT DATA
        header.setAttribute('idchat', data.id)
        header.innerHTML = `
                <div class="default-user-state">
                    <div class="avatar-icon">
                        <img src="${avatarUrl}" alt="avatar" class="avatar-icon">
                    </div>
                    <div class="state default-user">
                        <div class="state-circle default-user ${receiverStatus}"></div>
                    </div>
                </div>
                <h1>${fullName}</h1>
        `;
        // Clean Message Div
        messagesDiv.innerHTML = ``
        data.messages.forEach(message => {
            let date = new Date(message.date);
            // Extraer la hora y los minutos
            let horas = date.getUTCHours(); // Usar getUTCHours() para obtener la hora en UTC
            let minutos = date.getUTCMinutes(); 
            var messageHTML = ''
            if (message.author == receiverId) {
                messageHTML += `
                <div class="message-row">
                    <div class="message left">
                    `
                    if (message.urlMedia != undefined) {
                        if (message.typeMedia == 'img') {
                            messageHTML += `
                            <div>
                                    <div class="media">
                                        <img src="${message.urlMedia}" class="media">
                                    </div>
                                </div>
                            `
                        }
                        else {
                            messageHTML += `
                            <div>
                                    <div class="media">
                            <video controls class="media">
                                <source class="media" src="${message.urlMedia}" type="video/mp4">
                                <source class="media" src="${message.urlMedia}" type="video/avi">
                                Tu navegador no soporta la reproducción de videos.
                            </video>
                            </div>
                            </div>
                            `

                        }
                    }
                        
                messageHTML += `
                        <div class="message-body">
                            <div class="content">
                                ${message.content}
                            </div>
                            <div class="date">
                                ${horas}:${minutos}
                            </div>
                        </div>
                    </div>
                </div>
                `
            } else {
                messageHTML += `
                <div class="message-row">
                    <div class="message right">
                    `
                    if (message.urlMedia != undefined) {
                        if (message.typeMedia == 'img') {
                            messageHTML += `
                            <div>
                                    <div class="media">
                                        <img src="${message.urlMedia}" class="media">
                                    </div>
                                </div>
                            `
                        }
                        else {
                            messageHTML += `
                            <div>
                                    <div class="media">
                            <video controls class="media">
                                <source class="media" src="${message.urlMedia}" type="video/mp4">
                                <source class="media" src="${message.urlMedia}" type="video/avi">
                                Tu navegador no soporta la reproducción de videos.
                            </video>
                            </div>
                            </div>
                            `

                        }
                    }
                            
                    messageHTML += `
                        <div class="message-body">
                            <div class="content">
                                ${message.content}
                            </div>
                            <div class="date">
                                ${horas}:${minutos}
                            </div>
                        </div>
                    </div>
                </div>
                `
            }
            messagesDiv.innerHTML += messageHTML
        });
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        info.style.display = 'none'
        input.style.display = 'flex'
        send.setAttribute('idchat',data.id)
        send.setAttribute('fullname',fullName)
        send.setAttribute('receiverid',receiverId)
    })
}


export function addMessages(){
    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    const id = document.getElementById('chat-header').getAttribute('idchat');
    var input_content = document.getElementById('message-input')
    var content = input_content.value

    const mediaInput = document.getElementById('input-media');
    const media = mediaInput.files[0];
    const formData = new FormData();
    formData.append('id', id);
    formData.append('content', content);
    formData.append('media', media);

    
    fetch(`${dominioBase}/chat/add/messages/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
    })
    .catch(error => {
        console.error('Error al enviar el mensaje:', error);
    });
}

// Send message with Enter
document.getElementById("message-input").addEventListener("keyup", function(event) {
    if (event.key === "Enter") { // Verifica si la tecla presionada es "Enter"
        event.preventDefault(); // Evita que el formulario se envíe
        document.getElementById("send").click(); // Simula un clic en el botón
      }
  });
document.getElementById("send").addEventListener("click", addMessages)