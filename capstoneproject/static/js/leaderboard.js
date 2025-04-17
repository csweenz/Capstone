document.addEventListener("DOMContentLoaded", function(){
  const container = document.querySelector('.leaderboard-container');
  if (!container) return;

  // wheel → horizontal
  container.addEventListener('wheel', e => {
    if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
      e.preventDefault();
      container.scrollLeft += e.deltaY;
    }
  }, { passive: false });

  // scroll wheel
  let isDown = false, startX, scrollLeft;
  container.addEventListener('mousemove', e => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - container.offsetLeft;
    container.scrollLeft = scrollLeft - (x - startX);
  });
});

