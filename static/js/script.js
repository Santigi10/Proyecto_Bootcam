document.addEventListener('DOMContentLoaded', function () {
  const ctx = document.getElementById('graficoEnergias').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Eólica', 'Solar', 'Hidráulica', 'Geotérmica'],
      datasets: [{
        label: 'Producción de Energía (en MW)',
        data: [50, 75, 60, 30],
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
});
