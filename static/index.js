
function sub(event) {

  var formData = new FormData();
  document.getElementById("modal-body").innerText="LOADING ..."
  
  // Get the file input element
  var fileInput = document.getElementById("fileToUpload");
  
  // Add the file to the FormData object
  formData.append("file", fileInput.files[0]);
  
  // Send the AJAX request with the FormData object
  $.ajax({
    url: "/",
    method: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (response) {
      console.log(response.result);
      document.getElementById("modal-body").innerText=response.result
    },
    error: function (xhr, status, error) {
      console.log(error)
    }
  });
}


function previewImage(event) {
  var reader = new FileReader();
  reader.onload = function () {
    var output = document.getElementById("previewImage");
    output.style.visibility = "visible";
    output.src = reader.result;
  };
  reader.readAsDataURL(event.target.files[0]);
}

function handleFiles(files) {
  var file = files[0];
  var reader = new FileReader();

  reader.onload = function (e) {
    var img = new Image();
    img.src = e.target.result;

    // Add image to page
    dropzone.appendChild(img);
  };

  reader.readAsDataURL(file);
}
