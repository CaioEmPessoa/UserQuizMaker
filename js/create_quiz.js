// the slider output <--------------------------------------------------<
let slider = document.getElementById("questionSlider");
let output = document.getElementById("sliderOutput");
output.innerHTML = slider.value // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
var qstn_ammount = 5
slider.oninput = function() {
  qstn_ammount = this.value
  output.innerHTML = this.value
}
// >----------------------------------------------------> END SLIDER

// START json data <------------------------------------------------------------------------------<
let send_button = document.getElementById("enviar");
let loading = document.getElementById("loading")
let error_label = document.getElementById("error")

send_button.onclick = function(){
  let nameEntry = document.getElementById("usernameEntry").value

  if (nameEntry[nameEntry.length-1] != "/"){
    nameEntry = nameEntry + "/"
  }

  // split link and get the last part of it (name or id)

  nameEntry = nameEntry.split("/")
  nameEntry = nameEntry[nameEntry.length-2]
  
  if(nameEntry==undefined || nameEntry==""){
    return error_label.innerHTML = "Insira um link válido."
  }

  send_button.style.display = "none"
  loading.style.display = "inline-block"

  if (qstn_ammount==0){
    qstn_ammount = 1
  }
  
  fetch('https://steam-quiz-api.onrender.com/steam_app/test')
  .then( response => {
    fetch("https://steam-quiz-api.onrender.com/steam_app/create/" + nameEntry + "/" + qstn_ammount).then(response => response.json()).then(
      function(data){
        // se o data retornar um erro, ele mostra o erro.
        if(data["status"] != "Quiz Criado!"){
          send_button.style.display = "inline-block"
          loading.style.display = "none"
          document.getElementById("error").innerHTML = data["status"]
          return
          
        } 
        if (data["status"] == "Quiz Criado!") {
          document.getElementById("error").style.color = "lime"
          let sharelink = document.getElementById("sharelink")

          error_label.innerHTML = "Quiz feito! Você pode acessar ou compartilhar ele no seguinte link:"
          sharelink.innerHTML = "https://caioempessoa.github.io/UserQuizMaker/view/quiz.html?id="+ data["qstn_id"]
          sharelink.href = "https://caioempessoa.github.io/UserQuizMaker/view/quiz.html?id="+ data["qstn_id"]
          
          send_button.style.display = "inline-block"
          loading.style.display = "none"
          return
        }
      });
    })
    .catch(error => {
      send_button.style.display = "inline-block"
      loading.style.display = "none"
      return error_label.innerHTML = "Erro do servidor, tente novamente mais tarde."
    });
  }
  //>-----------------------------------------------------------------------------> END json data
  

// help button <--------------------------------<
let helpBtn = document.getElementById("info-btn")
let helpDiv = document.getElementById("ajuda-oculta")
// false bc it doesn't show up
let state = false

helpBtn.onclick = function(){
  if(state==false){
  helpDiv.style.display = "inline"
  // it is now showing
  state = true
} else{
  helpDiv.style.display = "none"
  // it isn't showing anymore
  state = false
}}
// >--------------------------==> END help button
