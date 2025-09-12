fetch('/api/message')
  .then(response => response.json())
  .then(data => {
    document.getElementById('mensaje').textContent = data.message;
  })
  .catch(error => {
    console.error('Error al obtener el mensaje:', error);
  });
