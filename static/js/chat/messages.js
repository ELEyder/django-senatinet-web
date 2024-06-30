import { db } from '../firebaseConfig.js';

const dominioBase = window.location.origin;

export function loadMessages(event){
    var button = event.currentTarget;
    var idChat = button.getAttribute('idchat')
    var fullName = button.getAttribute('fullname')
    var avatarUrl = button.getElementsByTagName('img')[0].getAttribute('src')
    var receiverId = button.getAttribute('receiverid')
    var receiverStatus = button.getAttribute('receiverStatus')

    var info = document.getElementById('info')
    var input = document.getElementById('input-chat')
    var send = document.getElementById('send')
        db.collection(`chats/${idChat}/messages`).orderBy('date')
        .onSnapshot(snapshot => {
            const messagesDiv = document.getElementById('chat-details');
            const header = document.getElementById('chat-header');
            header.setAttribute('idchat', idChat)
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
            messagesDiv.innerHTML = ``
            snapshot.forEach(doc => {
                const message = doc.data();
                const messageDate = message.date.toDate();
                var horas = messageDate.getHours(); // Obtiene las horas (formato de 0 a 23)
                var minutos = messageDate.getMinutes();
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
            send.setAttribute('idchat',idChat)
            send.setAttribute('fullname',fullName)
            send.setAttribute('receiverid',receiverId)
        }, error => {
            console.error('Error al cargar los mensajes:', error);
        });
}

export function sendMessage(){
    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    const dominioBase = window.location.origin;

    const id = document.getElementById('chat-header').getAttribute('idchat');
    var input_content = document.getElementById('message-input')
    var content = input_content.value

    const archivoInput = document.getElementById('input-media');
    const media = archivoInput.files[0];
    const formData = new FormData();
    formData.append('content', content);

    formData.append('media', media);

    
    fetch(`${dominioBase}/chat/${id}/send/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    })
    .then(response => {
        console.log('Respuesta del servidor:', response);
        input_content.value = ""
        archivoInput.value = null
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
document.getElementById("send").addEventListener("click", sendMessage)