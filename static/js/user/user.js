function sendRequest(button){
	var username = button.getAttribute('username')
	var idUser = button.getAttribute('idUser')
	var fStatus = button.getAttribute('state')

    const dominioBase = window.location.origin;

    if (fStatus == 'View'){
        window.location.href = `${dominioBase}/user/@${username}`
    } else if (fStatus == 'Send'){
        fetch(`${dominioBase}/user/friendRequest/${idUser}`)
        alert("Solicitud Enviada")
        button.setAttribute('state', 'Cancel');
        button.innerText = 'Cancel';
    } else if (fStatus == 'Cancel'){
        fetch(`${dominioBase}/user/friendRequest/${idUser}`)
        alert("Solicitud Cancelada")
        button.setAttribute('state', 'Send');
        button.innerText = 'Send';
    } else {
        fetch(`${dominioBase}/user/friendRequest/${idUser}`)
        alert("Solicitud Aceptada")
        button.setAttribute('state', 'View');
        button.innerText = 'View';
    }
}