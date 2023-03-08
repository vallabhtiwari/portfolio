var fileForm = document.getElementById("form")
var modalLink = document.getElementById("modal-link")
fileForm.addEventListener("submit", function(event) {
  event.preventDefault()
  var formdata = new FormData(fileForm)
  fileForm.reset()
  var url = `${window.location.href}`
  fetch(url, {
    method: "POST",
    body: formdata,
  })
    .then((response) => response.json())
    .then((data) => {

      url = "/share/upload-success/" + data["folder_id"]

      fetch(url, {
        method: "GET",
      })
        .then((response) => response.json())
        .then((data) => {
          modalLink.innerText = data["url"]
          document.getElementById("modal-button").click()
        })
    })
})

document.getElementById("clip").addEventListener("click", function() {
  navigator.clipboard.writeText(modalLink.innerText)
  document.getElementById("clip-icon").className = "bi bi-clipboard-check"
})

