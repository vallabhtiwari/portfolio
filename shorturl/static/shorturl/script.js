var fileForm = document.getElementById("form")
var urlContent = document.getElementById("url-content")
var clip = document.getElementById("clip")
var errorMess = document.getElementById("error")
var mess = document.getElementById("note")

fileForm.addEventListener("submit", function(event) {
  event.preventDefault()
  var formdata = new FormData(fileForm) // data to be sent to the server

  fileForm.reset()
  var url = "/shorten/url/"

  errorMess.classList.add("d-none")
  document.getElementById("clip-icon").className = "bi bi-clipboard"

  axios.post(url, formdata)
    .then(function(response) {
      clip.classList.remove("d-none")
      mess.classList.remove("d-none")
      urlContent.innerText = response.data["url"]
    })
    .catch(function(error) {
      insertError(error.response.data["message"])
    });
})

clip.addEventListener("click", function() {
  navigator.clipboard.writeText(urlContent.innerText)
  document.getElementById("clip-icon").className = "bi bi-clipboard-check"
})

function insertError(message) {
  errorMess.innerHTML = `
      <strong> <i class="bi bi-exclamation-triangle-fill">
        </i> Error:
      </strong> ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      `
  errorMess.classList.remove("d-none")
}
