function showOverlay(){
    var overlay = document.getElementById('overlay')
    overlay.style.width = '400px'
}
function closeOverlay(){
    overlay.style.width = '0px'
}

document.getElementById('showOverlay').addEventListener('click', showOverlay)
document.getElementById('closeOverlay').addEventListener('click', closeOverlay)