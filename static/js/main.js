function like(button){
	var idPost = button.getAttribute('id-post')
	var likes = parseInt(button.getAttribute('likes'))
	var isActive = button.classList.contains("active");

    button.classList.toggle("active", !isActive);
    button.classList.toggle("inactive", isActive);

    likes += isActive ? -1 : 1;
    button.setAttribute('likes', likes);
    button.innerText = `Likes: ${likes}`;

	fetch(`post/like/${idPost}`)
	return false;
}