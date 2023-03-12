async function getDataFromPython() {
    document.getElementById('prod').innerText = await eel.items()();
}

document.getElementById('itembtn').addEventListener('click', () {
    getDataFromPython
})