document.addEventListener('DOMContentLoaded', function() {
    // Get today's date in YYYY-MM-DD format
    const today = new Date().toISOString().split('T')[0];

    // Set the min attribute for start_date and end_date inputs
    document.getElementById('start_datepick').setAttribute('min', today);
    document.getElementById('end_datepick').setAttribute('min', today);
});