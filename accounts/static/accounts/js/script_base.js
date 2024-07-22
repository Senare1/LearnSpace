function addOption(button) {
    const inputGroup = button.closest('.input-group');
    const input = inputGroup.querySelector('input');
    const optionText = input.value.trim();

    if (optionText) {
        const newOptionDiv = document.createElement('div');
        newOptionDiv.classList.add('form-check');

        const newOptionInput = document.createElement('input');
        newOptionInput.classList.add('form-check-input');
        newOptionInput.type = 'checkbox';
        newOptionInput.id = optionText;
        newOptionInput.value = optionText;

        const newOptionLabel = document.createElement('label');
        newOptionLabel.classList.add('form-check-label');
        newOptionLabel.htmlFor = optionText;
        newOptionLabel.innerText = optionText;

        newOptionDiv.appendChild(newOptionInput);
        newOptionDiv.appendChild(newOptionLabel);

        const qcmOptions = document.getElementById('qcmOptions');
        qcmOptions.appendChild(newOptionDiv);

        input.value = '';
    }
}

function saveAndCloseModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.hide();
}

function resetForm(formId) {
    document.getElementById(formId).reset();
    const qcmOptions = document.getElementById('qcmOptions');
    qcmOptions.innerHTML = `
        <div class="input-group mb-2">
            <input type="text" class="form-control" placeholder="Entrez une réponse">
            <div class="input-group-append">
                <button class="btn btn-outline-secondary" type="button" onclick="addOption(this)">Ajouter</button>
            </div>
        </div>`;
}
