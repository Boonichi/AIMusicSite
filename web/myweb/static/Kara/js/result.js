const url = 'http://127.0.0.1:8000/Kara/api/getjson/'

var play=0;
var audio = document.getElementById("audioFile");
var button =document.getElementById('play');
var V = audio.volume;
var result;
var totalTime = parseInt(audio.duration * 1000);
var timeList = [];
var safeKill = 0;
var counter = 0;
var time = 0;
var previousTime;

function processTime(a) {
  var b = parseInt(a / 60000);
  var c = parseInt((a % 60000) / 1000);
  if (c < 10) {
    c = "0" + c;
  }
  return b + ":" + c;
}

function centerize() {
  if (play == 0) return;
  if ($(".current").length == 0) return;
  var a = $(".current").height();
  var c = $("#lyrics").height();
  var d =
    $(".current").offset().top - $(".current").parent().offset().top;
  var e = d + a / 2 - (c * 1) / 4;
  $("#lyrics").animate(
    { scrollTop: e + "px" },
    { easing: "swing", duration: 500 }
  );
}

function setArtistName(artistName){
  var context = $('.artist-name');
  for(var i=0;i<context.length;i++){
      context[i].innerHTML = artistName;
  }
};


function setSongName(songName){
  var context = $('.song-name');
  for(var i=0;i<context.length;i++){
    context[i].innerHTML = songName;
  }
};

function processing(data) {
  setArtistName(data.author_name);
  setSongName(data.song_name);
  var html = "";
  timeList = [];
  for (var i = 0; i < data.lyrics.length; i++) {
    timeList.push(data.lyrics[i].s);
    html = html + "<h2>" + data.lyrics[i].sentence + "</h2>";
  }
  $("#lyrics-content").html(html);
  $("#totalTime").html(processTime(totalTime));
  $("#currentTime").html(processTime(time));
  var percent = (time / totalTime) * 100;
  $("#progress").css("width", percent + "%");
};

function changeProgress() {
  dragHandler = (event) => {
    event.preventDefault;
    if (event.offsetY > 5 || event.offsetY < 1) return;
    var width = $("#progress-bar").css("width");
    var percent = (parseInt(event.offsetX) / parseInt(width)) * 100;
    $("#progress").css("width", percent + "%");
    time = parseInt(totalTime * (percent / 100));
    audio.currentTime = parseInt(time / 1000);
  };
}
$("#progressButton").on("mousedown", changeProgress());
$("#progress-bar").mouseup(function () {
  $("#progress-bar").off("mousemove");
});
$("#progressButton").mouseup(function () {
  $("#progress-bar").off("mousemove");
});

function playSong(){
  if (play == 0) {
    play = 1;
    audio.play();
    $("#menu button#play i").removeClass("fa-play");
    $("#menu button#play i").addClass("fa-pause");
  } else {
    play = 0;
    audio.pause();
    $("#menu button#play i").removeClass("fa-pause");
    $("#menu button#play i").addClass("fa-play");
  }
};

function reset() {
  time = 0;
  audio.currentTime = 0;
}

function previous() {
  var current = $("#lyrics .current");
  if (current.length == 0) {
    return;
  }
  var first = $("#lyrics-content h2:nth-child(1)");
  current.removeClass("current");
  if (current === first) {
    return;
  }
  current.prev().addClass("current");
}

function next() {
  var current = $("#lyrics .current");
  if (current.length == 0) {
    $("#lyrics-content h2:nth-child(1)").addClass("current");
    return;
  }
  current.removeClass("current");
  current.next().addClass("current");
}

function updateTimer(data) {
  if (totalTime == 0 || isNaN(totalTime)) {
    totalTime = parseInt(audio.duration * 1000);
    processing(data);
  }
  //for the end of the song
  if (time >= totalTime) {
    if (play == 0) return;
    playSong();
    if (songRepeat == 1) {
      reset();
      playSong();
      return;
    } else {
      nextSong();
      playSong();
    }
    return;
  }
  //update timer
  if (play == 1) {
    time = time + 1000;
  } else if (play == -1) {
    time = 0;
  }
  //upadate time on the progress bar
  if (audio.currentTime != previousTime) {
    previousTime = audio.currentTime;
    $("#currentTime").html(processTime(time));
    var percent = (time / totalTime) * 100;
    $("#progress").css("width", percent + "%");
  } else {
    time = parseInt(audio.currentTime * 1000);
    // if (time > 100) time = time - 100;
    if (play == 1) {
      audio.pause();
      if (audio.readyState == 4) {
        audio.play();
      }
    }
  }
  safeKill = 0;
  while (true) {
      safeKill += 1;
      if (safeKill >= 100) break;
      if (counter == 0) {
        if (time < timeList[counter]) {
          previous();
          break;
        }
      }
      if (counter == timeList.length && time <= timeList[counter - 1]) {
        counter--;
        previous();
      }
      if (time >= timeList[counter]) {
        if (counter <= timeList.length) {
          counter++;
        }
        next();
      } else if (time < timeList[counter - 1]) {
        counter--;
        previous();
      } else {
        if (play == 1 && !audio.paused && !audio.ended) centerize();
        break;
      }
  }
}

$("#progress-bar").on("mousedown", function () {
  $("#progress-bar").on("mousemove", function handler(event) {
    event.preventDefault;
    if (event.offsetY > 5 || event.offsetY < 1) return;
    var width = $("#progress-bar").css("width");
    var percent = (parseInt(event.offsetX) / parseInt(width)) * 100;
    $("#progress").css("width", percent + "%");
    time = parseInt(totalTime * (percent / 100));
    audio.currentTime = parseInt(time / 1000);
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  } 
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

async function main(){
  try{
      const  response=await fetch(url,{
          method:'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken,
          },           
          mode: 'same-origin'
      });
      res= await response.json();
      result=JSON.parse(res.data);
      processing(result)
  }catch(e){
      console.log(e)
  }
};

main()

$("#up").on("click",function(){
    if(V<1){
        V +=0.1;
        audio.volume=V;
    }
});
$("#down").on("click",function(){
    if(V>0){
        V -=0.1;
        audio.volume=V;
    }
});
$("#next").on("click",function(){
    if(time < totalTime){
        time += 5000;
        audio.currentTime = parseInt(time/1000)
    }
});
$("#prev").on("click",function(){
    if(time>5100){
        time -= 5000;
        audio.currentTime = parseInt(time/1000)
    }
});

button.addEventListener('click',event => {
  playSong();
});

stopTimer = setInterval(function () {
  updateTimer(result);
}, 1000);
