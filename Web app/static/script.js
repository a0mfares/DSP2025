document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', function () {
      // Create loading overlay
      const loadingOverlay = document.createElement('div');
      loadingOverlay.className = 'loading-overlay';

      const spinnerContainer = document.createElement('div');
      spinnerContainer.style.display = 'flex';
      spinnerContainer.style.alignItems = 'center';

      const spinner = document.createElement('div');
      spinner.className = 'spinner';

      const loadingText = document.createElement('div');
      loadingText.textContent = 'Processing audio...';

      spinnerContainer.appendChild(spinner);
      spinnerContainer.appendChild(loadingText);
      loadingOverlay.appendChild(spinnerContainer);

      document.body.appendChild(loadingOverlay);
    });
  }

  // Toggle advanced parameters
  const toggleButtons = document.querySelectorAll('.toggle-params');
  toggleButtons.forEach(button => {
    button.addEventListener('click', function () {
      const targetId = this.getAttribute('data-target');
      const targetElement = document.getElementById(targetId);
      if (targetElement) {
        targetElement.classList.toggle('d-none');
        this.textContent = targetElement.classList.contains('d-none') ?
          'Show Advanced Parameters' : 'Hide Advanced Parameters';
      }
    });
  });

  // Update filter parameter visibility based on filter type
  const filterTypeSelect = document.getElementById('filter_type');
  if (filterTypeSelect) {
    const updateFilterParams = function () {
      const filterType = filterTypeSelect.value;
      const rippleGroup = document.getElementById('ripple-group');
      const attenuationGroup = document.getElementById('attenuation-group');

      if (filterType === 'butter' || filterType === 'fir') {
        rippleGroup.style.display = 'none';
        attenuationGroup.style.display = 'none';
      } else if (filterType === 'cheby1') {
        rippleGroup.style.display = 'block';
        attenuationGroup.style.display = 'none';
      } else if (filterType === 'cheby2') {
        rippleGroup.style.display = 'none';
        attenuationGroup.style.display = 'block';
      } else if (filterType === 'ellip') {
        rippleGroup.style.display = 'block';
        attenuationGroup.style.display = 'block';
      }
    };

    filterTypeSelect.addEventListener('change', updateFilterParams);
    // Initialize on page load
    updateFilterParams();
  }
});