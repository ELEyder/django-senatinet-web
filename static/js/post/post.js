function like(button){
	var idPost = button.getAttribute('id-post')
	var likes = parseInt(button.getAttribute('likes'))
	var isActive = button.classList.contains("active");
    playLike()
    button.classList.toggle("active", !isActive);
    button.classList.toggle("inactive", isActive);

    likes += isActive ? -1 : 1;
    button.setAttribute('likes', likes);
    button.innerText = `Likes: ${likes}`;
    const dominioBase = window.location.origin;
	fetch(`${dominioBase}/post/like/${idPost}`)
	return false;
}

function goComment(elemento){
    var id = elemento.getAttribute('idPost')
    var input = document.getElementById(id)
    input.focus()
}