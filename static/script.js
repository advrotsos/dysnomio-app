function toggleDialog(dialogId) {
  var dialog = document.getElementById(dialogId);
  if (dialog.open) {
      dialog.classList.remove('show-dialog'); // Remove the class to hide the dialog
      dialog.close();
  } else {
      dialog.open = true;
      dialog.classList.add('show-dialog'); // Add the class to show the dialog with animation
  }
}
