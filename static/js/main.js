async function like(button){
	var idPost = button.getAttribute('id-post')
	var likes = button.getAttribute('likes')
	likes = parseInt(likes)
	try{
		var nya = await fetch(`/like/${idPost}`)
		console.log(nya)
	}
	catch(error){
		console.log('Error:', error)
	} 

	if (button.classList.contains("active")) {
		button.classList.remove("active");
		button.classList.add("inactive");
		likes -= 1
		button.setAttribute('likes', likes)
		button.innerText = "Likes: " + likes;
	} else {
		button.classList.remove("inactive");
		button.classList.add("active");
		likes += 1
		button.setAttribute('likes', likes)
		button.innerText = "Likes: " + likes;
	}
}