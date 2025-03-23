document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');
    const filtersSelect = document.getElementById('id_filters');

    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            const categoryId = this.value;
            if (categoryId) {
                fetch(`/admin/get-subcategories/?category_id=${categoryId}`)
                    .then(response => response.json())
                    .then(data => {
                        subcategorySelect.innerHTML = '<option value="">---------</option>';
                        data.forEach(subcategory => {
                            const option = document.createElement('option');
                            option.value = subcategory.id;
                            option.textContent = subcategory.name;
                            subcategorySelect.appendChild(option);
                        });
                    });

                fetch(`/admin/get-filters/?category_id=${categoryId}`)
                    .then(response => response.json())
                    .then(data => {
                        filtersSelect.innerHTML = '';
                        data.forEach(filter => {
                            const option = document.createElement('option');
                            option.value = filter.id;
                            option.textContent = filter.name;
                            filtersSelect.appendChild(option);
                        });
                    });
            }
        });
    }
});