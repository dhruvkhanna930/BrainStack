function copyToClipboard(value) {
  // Create a temporary textarea element
  var textarea = document.createElement('textarea');

  // Set the value of the textarea
  textarea.value = value;

  // Append the textarea to the document
  document.body.appendChild(textarea);

  // Select and copy the text inside the textarea
  textarea.select();
  document.execCommand('copy');

  // Remove the textarea from the document
  document.body.removeChild(textarea);
}

// Example variable
var ul = "This is the value of the variable 'ul'.";

// Copy the value of 'ul' to the clipboard
copyToClipboard(ul);