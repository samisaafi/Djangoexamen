console.log("Dark theme script loaded!");
document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.main-header');
    if (header) {
        header.style.backgroundColor = '#222';
        header.style.color = 'white';
    }
});