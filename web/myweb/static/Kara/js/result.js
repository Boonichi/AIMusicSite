const url = 'http://127.0.0.1:8000/Kara/api/getjson/'



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

  function loadSong() {
        $("#audioFile").attr("src", 'static/TaDaTungYeuNhauChua-Hao-6248598.mp3');
        // abort_other_json = $.getJSON('result.json', function (data) {
        //   processing(data);
        //   totalTime = NaN;
        //   stopTimer = setInterval(function () {
        //     updateTimer(data);
        //   }, 1000);
        // });
  }

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
      }
function setArtistName(artistName){
        var context = $('.artist-name');
        for(var i=0;i<context.length;i++){
            context[i].innerHTML = artistName;
        }
}
function setSongName(songName){
  var context = $('.song-name');
  for(var i=0;i<context.length;i++){
      context[i].innerHTML = songName;
  }
}
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
      res= await response.json()
      result=JSON.parse(res.data)
      console.log(result)
      processing(result)
      
  }catch(e){
      console.log(e)
  }
}

main()




  function loadSong() {
        $("#audioFile").attr("src", indexing.audio);
        abort_other_json = $.getJSON('result.json', function (data) {
          processing(data);
          totalTime = NaN;
          stopTimer = setInterval(function () {
            updateTimer(data);
          }, 1000);
        });
  }