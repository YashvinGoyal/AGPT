var stripContent = document.querySelector('.strip-content');

stripContent.addEventListener('mouseover', function() {
  stripContent.style.animationPlayState = 'paused';
});

stripContent.addEventListener('mouseout', function() {
  stripContent.style.animationPlayState = 'running';
});