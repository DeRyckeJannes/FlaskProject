function updateTime() {
    var currentTime = new Date();
    var hours = currentTime.getHours();
    var minutes = currentTime.getMinutes();
    var tijd = hours + ":" + minutes + " ";
    var pElement=document.getElementById('pTijd');
    pElement.innerHTML=tijd;
}
setInterval(updateTime,100);
