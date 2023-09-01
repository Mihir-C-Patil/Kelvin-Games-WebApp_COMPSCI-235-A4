const progressBar = document.querySelector('.progress-bar');

window.addEventListener('scroll', () => {
    const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
    progressBar.style.height = `${scrolled}%`;
});
