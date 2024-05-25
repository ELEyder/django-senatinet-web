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

function loadMessages(id){
    idGlobal = id;
    db.collection(`chats/${id}/messages`)
        .onSnapshot(snapshot => {
            const messagesDiv = document.getElementById('chat-details');
            var receiverName = document.getElementById('receiverFullName').innerText
            messagesDiv.innerHTML = `
            <p>${receiverName}</p>
            `;
            
            snapshot.forEach(doc => {
                const message = doc.data();
                messagesDiv.innerHTML += `
                <div class="message">

                <strong>${message.author}:</strong>
                ${message.content} <br>
                </div>
                `;
                // <small>${message.date}</small>
            });
            
            messagesDiv.innerHTML += '</ul>';
        }, error => {
            console.error('Error al cargar los mensajes:', error);
        });
}

function sendMensaje(author){
    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    const dominioBase = window.location.origin;
    const id = document.getElementById('chat-details').getAttribute('idChat');
    var input_content = document.getElementById('message-input')
    var content = input_content.value
    const messageData = {
        author: author,
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
        loadMessages(id);

    })
    .catch(error => {
        console.error('Error al enviar el mensaje:', error);
    });
}
