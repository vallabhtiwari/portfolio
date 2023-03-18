var fileForm = document.getElementById("form")
var modalLink = document.getElementById("modal-link")
var galati = 0
fileForm.addEventListener("submit", function(event) {
  event.preventDefault()
  var formdata = new FormData(fileForm) // data to be sent to the server

  // checking file size
  var totalSize = 0
  for (var f of formdata) {
    if (typeof f[1].size == "number")
      totalSize += f[1].size

    if (f[1].size > 200000000 || totalSize > 200000000) {
      dontSend()
      return
    }
  }
  // toggling the form validation errors
  document.getElementById("instructions").classList.remove("text-danger")
  document.getElementById("id_file").classList.remove("is-invalid")
  fileForm.reset()
  var url = "/share/upload/"

  // progress-bar and headers
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

  // sending form data (post request)
  axios.post(url, formdata, config)
    .then(function(response) {

      // sending request to get the shortened url
      url = `/share/upload-success/${response.data["folder_id"]}`
      axios.get(url)
        .then(function(response) {
          modalLink.innerText = response.data["url"]
          document.getElementById("modal-button").click()
        })
        .catch(function(error) {
          insertError(error.response.data["message"])
        })
    })
    .catch(function(error) {
      insertError(error.response.data["message"])
    });
})

// copy to clipboard
document.getElementById("clip").addEventListener("click", function() {
  navigator.clipboard.writeText(modalLink.innerText)
  document.getElementById("clip-icon").className = "bi bi-clipboard-check"
})

// removing the progress-bar when modal is closed
document.getElementById("modal-close-button").addEventListener("click", function() {
  document.getElementById("clip-icon").className = "bi bi-clipboard"
  document.getElementById("progress-bar-container").classList.add("d-none")
})

// form validation errors
function dontSend() {
  document.getElementById("instructions").classList.add("text-danger")
  document.getElementById("id_file").classList.add("is-invalid")
}

// inserting errors from server(if received)
function insertError(message) {
  var errorMess = document.getElementById("error")
  errorMess.innerHTML = `
      <strong> <i class="bi bi-exclamation-triangle-fill">
        </i> Error:
      </strong> ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      `
  errorMess.classList.remove("d-none")
}
