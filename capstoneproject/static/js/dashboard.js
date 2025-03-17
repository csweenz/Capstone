// for showing and hiding forms
  function toggleDisplay(id) {
    const element = document.getElementById(id);
    element.style.display = (element.style.display === 'block') ? 'none' : 'block';
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
  });