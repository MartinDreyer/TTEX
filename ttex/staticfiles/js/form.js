const text = document.getElementById("id_text");

text.cols = null;
text.rows = null;

const resizeTextArea = () => {
  text.style.height = "auto";
  text.style.height = text.scrollHeight + "px";
};

document.addEventListener("DOMContentLoaded", (event) => {
  resizeTextArea();
});
