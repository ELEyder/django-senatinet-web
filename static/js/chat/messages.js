const firebaseConfig = {
    apiKey: "AIzaSyARwSYWD_euCV_2qQ4sL2S6Vrj_p_b0j_I",
    authDomain: "mediasenati.firebaseapp.com",
    projectId: "mediasenati",
    storageBucket: "mediasenati.appspot.com",
    messagingSenderId: "147613346111",
    appId: "1:147613346111:web:a349302d624f17b5580b8a"
};

firebase.initializeApp(firebaseConfig);

// Obtiene una referencia a la colección de mensajes
const db = firebase.firestore();

function loadMessages(event){
    var button = event.currentTarget;
    var idChat = button.getAttribute('idchat')
    var fullName = button.getAttribute('fullname')
    var avatarUrl = button.getElementsByTagName('img')[0].getAttribute('src')
    var receiverId = button.getAttribute('receiverid')

    var info = document.getElementById('info')
    var input = document.getElementById('input-chat')
    var send = document.getElementById('send')
        db.collection(`chats/${idChat}/messages`).orderBy('date')
        .onSnapshot(snapshot => {
            const messagesDiv = document.getElementById('chat-details');
            const header = document.getElementById('chat-header');
            header.setAttribute('idchat', idChat)
            header.innerHTML = `
                    <div class="avatar-icon">
                        <img src="${avatarUrl}" alt="avatar" class="avatar-icon">
                    </div>
                    <h1>${fullName}</h1>
            `;
            messagesDiv.innerHTML = ``
            snapshot.forEach(doc => {
                const message = doc.data();
                const messageDate = message.date.toDate();
                var horas = messageDate.getHours(); // Obtiene las horas (formato de 0 a 23)
                var minutos = messageDate.getMinutes();
                if (message.author == receiverId) {
                    messagesDiv.innerHTML += `
                    <div class="message-row">
                        <div class="message left">
                            <div class="content">
                            ${message.content}
                            </div>
                            <div class="date">
                            ${horas}:${minutos}
                            </div>
                        </div>
                    </div>
                    `
                } else {
                    messagesDiv.innerHTML += `
                    <div class="message-row">
                        <div class="message right">
                            <div class="content">
                            ${message.content}
                            </div>
                            <div class="date">
                            ${horas}:${minutos}
                            </div>
                        </div>
                    </div>
                    `
                }
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

function sendMensaje(){
    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    const dominioBase = window.location.origin;
    const id = document.getElementById('chat-header').getAttribute('idchat');
    var input_content = document.getElementById('message-input')
    var content = input_content.value
    const messageData = {
        content: content,
    };
    fetch(`${dominioBase}/chat/${id}/send/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(messageData),
    })
    .then(response => {
        console.log('Respuesta del servidor:', response);
        input_content.value = ""

    })
    .catch(error => {
        console.error('Error al enviar el mensaje:', error);
    });
}

document.getElementById("message-input").addEventListener("keyup", function(event) {
    if (event.key === "Enter") { // Verifica si la tecla presionada es "Enter"
        event.preventDefault(); // Evita que el formulario se envíe
        document.getElementById("send").click(); // Simula un clic en el botón
      }
  });

function addChat(event){
    const dominioBase = window.location.origin;
    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    var button = event.currentTarget;
    var id = button.getAttribute('idFriend')
    const messageData = {
        friend: id,
    };
    db.collection(`chats`)
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
        console.log('Respuesta del servidor:', data);
        if (!data.response) {
            const element = document.querySelector(`[idchat="${data.idchat}"]`);
            element.click()
        }
        closeOverlay()
    })
    .catch(error => {
        console.error('Error al enviar el mensaje:', error);
    });
}

function loadChats(){
    const dominioBase = window.location.origin;
    fetch(`${dominioBase}/chat/get`, {
        method: 'GET'
    })
    .then(response => response.json()) // Procesar la respuesta como JSON
    .then(data => {
        var chatsBody = document.getElementById('chats-body')
        chatsBody.innerHTML = ''
        data.chats.forEach(chat => {
            var chatHtml = `
            <div idChat="${chat.id}" fullName="${chat.receiverFirstName} ${chat.receiverLastName}" receiverId="${chat.receiver}" class="btn-chat" onclick="loadMessages(event)">
                <div class="avatar-icon">
                    <img src="${chat.receiverUrlAvatar}" alt="avatar" class="avatar-icon">
                </div> 
                <p>${chat.receiverFirstName} ${chat.receiverLastName}</p>
            </div>
            `;
            chatsBody.innerHTML +=chatHtml
        });
        console.log('Respuesta del servidor:', data);
    })
    .catch(error => {
        console.error('Error al enviar el mensaje:', error);
    });
}
db.collection(`chats`).onSnapshot(snapshot =>{
    loadChats()
})

function showOverlay(){
    var overlay = document.getElementById('overlay')
    overlay.style.width = '400px'
}
function closeOverlay(){
    overlay.style.width = '0px'
}