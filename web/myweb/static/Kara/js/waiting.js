const url = 'http://146.190.99.213:8000/Kara/waiting/'
data={}
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
        let csrftoken =getCookie('csrftoken')
        const  response=await fetch(url,{
            method:'POST',
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json',
              "X-CSRFToken": csrftoken,
            //   'X-CSRFToken' : csrftoken
              // 'Content-Type': 'application/x-www-form-urlencoded',
            },           
            mode: 'same-origin'
        });
        if(response.redirected==true){
          location.replace(response.url);
        }
    }catch(e){
        console.log(e)
    }

}

setTimeout(main,2000)