/**
 * Initializes and manages date pickers for the rental period, setting constraints on date selection.
 * Ensures the start date cannot be set in the past and the end date
 * is always set to at least one day after the start date.
 */
document.addEventListener('DOMContentLoaded', function() {
    /** @type {HTMLInputElement} */
    const startDateInput = document.getElementById('start_datepick');
    /** @type {HTMLInputElement} */
    const endDateInput = document.getElementById('end_datepick');

    /**
     * Sets the minimum selectable date for both start and end date inputs to today's date,
     * preventing users from selecting dates in the past.
     */
    function setMinDate() {
        const today = new Date().toISOString().split('T')[0];
        startDateInput.setAttribute('min', today);
        endDateInput.setAttribute('min', today);
    }

    // Initialize the minimum date settings for start and end date inputs.
    setMinDate();

    /**
     * Adds a specified number of days to a date and returns the new date.
     * @param {string} date - The starting date in YYYY-MM-DD format.
     * @param {number} days - The number of days to add to the date.
     * @returns {string} The new date in YYYY-MM-DD format after adding the specified number of days.
     */
    function addDaysToDate(date, days) {
        const result = new Date(date);
        result.setDate(result.getDate() + days);
        return result.toISOString().split('T')[0];
    }

    /**
     * Updates the minimum selectable end date based on the start date input's value.
     * This ensures the end date is at least one day after the start date.
     */
    startDateInput.addEventListener('change', function() {
        // Calculate and set the minimum end date to one day after the selected start date.
        const dayAfterStartDate = addDaysToDate(startDateInput.value, 1);
        endDateInput.setAttribute('min', dayAfterStartDate);
    });
});