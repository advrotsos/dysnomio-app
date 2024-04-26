function toggleDialog(dialogId) {
    var dialog = document.getElementById(dialogId);
    if (dialog.open) {
      dialog.close();
    } else {
      dialog.open = true;
    }
  }
