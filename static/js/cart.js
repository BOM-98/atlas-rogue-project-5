document.addEventListener("DOMContentLoaded", function () {

    // Remove item and reload on click
    $document.querySelectorAll('.remove-item').forEach(item => {
        item.addEventListener('click', function(e) {
            var csrfToken = "{{ csrf_token }}";
            var itemId = this.getAttribute('id').split('remove_')[1];
            var url = `/bag/remove/${itemId}`;
            var data = {'csrfmiddlewaretoken': csrfToken};
    
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(data)
            })
            .then(response => response.json())
            .then(data => {
                location.reload();
            })
            .catch(error => console.error('Error:', error));
        });
    });
});