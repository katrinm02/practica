const openModalBtn = document.getElementById('openModal');
const modal = document.getElementById('modal');
const closeBtn = modal.querySelector('.close');

openModalBtn.addEventListener('click', function() {
  modal.style.display = 'block';
});

closeBtn.addEventListener('click', function() {
  modal.style.display = 'none';
});

window.addEventListener('click', function(e) {
  if (e.target === modal) {
    modal.style.display = 'none';
  }
});

document.getElementById('dataForm').addEventListener('submit_form', function(event) {
    event.preventDefault();
    setTimeout(function() {
        window.location.href = 'index.html';
    }, 2000); 
});

function showInfo(personId) {
  var blocks = document.querySelectorAll('.hidden-block');
  blocks.forEach(function(block) {
    block.style.display = 'none';
  });
  document.getElementById(personId).style.display = 'block';
}