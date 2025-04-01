document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById('mental-health-form');

  form.addEventListener('submit', (event) => {
      event.preventDefault();
      alert('Thank you for submitting the questionnaire!');
  });
});
