function like(button){
	var idPost = button.getAttribute('id-post')
	var likes = parseInt(button.getAttribute('likes'))
	var isActive = button.classList.contains("active");

    button.classList.toggle("active", !isActive);
    button.classList.toggle("inactive", isActive);

    likes += isActive ? -1 : 1;
    button.setAttribute('likes', likes);
    button.innerText = `Likes: ${likes}`;
    const dominioBase = window.location.origin;
	fetch(`${dominioBase}/post/like/${idPost}`)
	return false;
}

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

function goComment(elemento){
    var id = elemento.getAttribute('idPost')
    var input = document.getElementById(id)
    input.focus()
}