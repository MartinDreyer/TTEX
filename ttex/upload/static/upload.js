function validateAudioFile(file) {
  const allowedTypes = [
    // Audio formats
    "audio/mpeg", // MP3
    "audio/wav", // WAV
    "audio/ogg", // OGG
    "audio/aac", // AAC
    "audio/flac", // FLAC
    "audio/webm", // WebM audio
    "audio/mp4", // MP4 audio

    // Video formats
    "video/mp4", // MP4
    "video/x-matroska", // MKV
    "video/webm", // WebM
    "video/ogg", // OGG
    "video/quicktime", // MOV
    "video/x-msvideo", // AVI
    "video/x-ms-wmv", // WMV
    "video/mpeg", // MPEG
  ];
  if (!allowedTypes.includes(file.type)) {
    alert("Forkert filtype. Kun lyd og videofiler er tilladt.");
    return false;
  }
  return true;
}
function displayFileName() {
  const fileInput = document.getElementById("audio_file");
  if (validateAudioFile(fileInput.files[0])) {
    const fileName = fileInput.files[0].name;
    const fileNameElement = document.getElementById("file_name");
    fileNameElement.textContent = fileName;

    const uploadInfo = document.getElementById("upload-info");
    uploadInfo.style.display = "none";
  }
}
