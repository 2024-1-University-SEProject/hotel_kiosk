document.addEventListener('DOMContentLoaded', function () {
    // Find all select elements except those already processed
    const selects = document.querySelectorAll('select:not(.custom-select-processed)');

    selects.forEach(select => {
        setupCustomSelect(select);
    });
});

function setupCustomSelect(select) {
    select.classList.add('custom-select-processed');
    select.style.display = 'none'; // Hide original select

    // Create wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'custom-select-wrapper';

    // Create trigger (the visible box)
    const trigger = document.createElement('div');
    trigger.className = 'custom-select-trigger';
    const selectedOption = select.options[select.selectedIndex];
    trigger.textContent = selectedOption ? selectedOption.textContent : 'Select...';

    // Add arrow icon using CSS or character
    // We'll handle arrow in CSS via ::after

    // Create options container
    const optionsList = document.createElement('div');
    optionsList.className = 'custom-options';

    // Populate options
    Array.from(select.options).forEach(option => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'custom-option';
        optionDiv.textContent = option.textContent;
        optionDiv.dataset.value = option.value;

        if (option.selected) {
            optionDiv.classList.add('selected');
        }

        optionDiv.addEventListener('click', function () {
            // Update UI
            trigger.textContent = this.textContent;
            optionsList.querySelectorAll('.custom-option').forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');

            // Close dropdown
            wrapper.classList.remove('open');

            // Update original select value
            select.value = this.dataset.value;

            // Trigger change/input events for listeners
            select.dispatchEvent(new Event('change', { bubbles: true }));
            select.dispatchEvent(new Event('input', { bubbles: true }));
        });

        optionsList.appendChild(optionDiv);
    });

    // Toggle dropdown
    trigger.addEventListener('click', function (e) {
        e.stopPropagation();
        // Close other open dropdowns
        document.querySelectorAll('.custom-select-wrapper.open').forEach(other => {
            if (other !== wrapper) other.classList.remove('open');
        });
        wrapper.classList.toggle('open');
    });

    // Assemble
    wrapper.appendChild(trigger);
    wrapper.appendChild(optionsList);

    // Insert after the select
    select.parentNode.insertBefore(wrapper, select.nextSibling);

    // Close when clicking outside
    document.addEventListener('click', function (e) {
        if (!wrapper.contains(e.target)) {
            wrapper.classList.remove('open');
        }
    });
}
