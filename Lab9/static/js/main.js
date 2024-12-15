document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('search-form');
    const spinner = document.getElementById('loading-spinner');
    const tableBody = document.querySelector('.students-table tbody');

    form.addEventListener('submit', async (event) => {

        spinner.style.display = 'block';
        event.preventDefault();

        const query = document.getElementById('query').value.trim();

        const url = new URL('/students', window.location.origin);
        const params = new URLSearchParams();
        if (query) params.append('query', query);
        url.search = params.toString();

        try {

            tableBody.innerHTML = '';

            const response = await fetch(url);
            const data = await response.json();

            if (!response.ok) {
                const error = data.error;

                if (error)
                     noResultRow.innerHTML = `<td colspan="3">${error}</td>`;

                throw new Error(`error: ${response.statusText}`);
            }

            const students = data.students || [];

            if (students.length > 0) {
                students.forEach(student => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${student.name}</td>
                        <td>${student.last_name}</td>
                        <td>${student.age || 'N/A'}</td>
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                const noResultRow = document.createElement('tr');

                tableBody.appendChild(noResultRow);
            }
        } catch (error) {
            console.error(error);
            alert('Nie udało się pobrać danych studentów.');
        }
        finally {
            spinner.style.display = 'none';
        }
    });
});