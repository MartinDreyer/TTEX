document.addEventListener("DOMContentLoaded", function () {
  const title = document.getElementById("id_title");
  if (title) {
    // Focus the input field to ensure the cursor is active in it
    title.focus();
    // Move the cursor to the end of the text
    const textLength = title.value.length;
    title.setSelectionRange(textLength, textLength);
  }
});
