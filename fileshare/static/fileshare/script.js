var fileForm = document.getElementById("form")
var modalLink = document.getElementById("modal-link")
fileForm.addEventListener("submit", function(event) {
  event.preventDefault()
  var formdata = new FormData(fileForm)
  fileForm.reset()
  var url = "/share/upload/"

  const config = {
    headers: {
      "Content-Type": "multipart/form-data"
    },
    onUploadProgress: function(progress) {
      var percent = (progress.loaded / progress.total) * 100
      percent = percent.toFixed(2)
      var progressBarContainer = document.getElementById("progress-bar-container")
      var progressBar = document.getElementById("progress-bar")
      progressBarContainer.classList.remove("d-none")
      progressBarContainer.setAttribute("aria-valuenow", percent)
      progressBar.style.width = `${percent}%`
    }
  }

  axios.post(url, formdata, config)
    .then(function(response) {
      url = "/share/upload-success/" + response.data["folder_id"]
      axios.get(url)
        .then(function(response) {
          modalLink.innerText = response.data["url"]
          document.getElementById("modal-button").click()
        })
        .catch(function(error) {
          console.log(error)
        })
    })
    .catch(function(error) {
      //handle error
      console.log(error);
    });
})

document.getElementById("clip").addEventListener("click", function() {
  navigator.clipboard.writeText(modalLink.innerText)
  document.getElementById("clip-icon").className = "bi bi-clipboard-check"
})
document.getElementById("modal-close-button").addEventListener("click", function() {
  document.getElementById("clip-icon").className = "bi bi-clipboard"
  document.getElementById("progress-bar-container").classList.add("d-none")
})
