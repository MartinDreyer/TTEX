function displayFileName() {
  const fileInput = document.getElementById("audio_file");
  const fileName = fileInput.files[0].name;
  const fileNameElement = document.getElementById("file_name");
  fileNameElement.textContent = fileName;

  const uploadInfo = document.getElementById("upload-info");
  uploadInfo.style.display = "none";
}
