// for showing and hiding forms
  function toggleDisplay(id) {
    const element = document.getElementById(id);
    element.style.display = (element.style.display === 'block') ? 'none' : 'block';
  }

  function toggleMenu() {
    const menu = document.getElementById('header-menu');
    menu.classList.toggle('show');
}

function toggleChat() {
    const chat = document.getElementById('chat-box');
    chat.classList.toggle('show');
}

// click listeners for update/delete functions
  document.querySelectorAll('.dashboard-data-row').forEach(row => {
    row.addEventListener('click', function() {
      const nextRow = this.nextElementSibling;
      if (nextRow && nextRow.classList.contains('dashboard-expand-row')) {
        // toggle display
        nextRow.style.display = (nextRow.style.display === 'table-row') ? 'none' : 'table-row';
      }
    });
  })

