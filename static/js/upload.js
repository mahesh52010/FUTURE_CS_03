document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('files');
    const fileNamesDiv = document.getElementById('file-names');

    input.addEventListener('change', function () {
        fileNamesDiv.innerHTML = '';
        if (input.files.length > 0) {
            const ul = document.createElement('ul');
            for (let i = 0; i < input.files.length; i++) {
                const li = document.createElement('li');
                li.textContent = input.files[i].name;
                ul.appendChild(li);
            }
            fileNamesDiv.appendChild(ul);
        }
    });
});
