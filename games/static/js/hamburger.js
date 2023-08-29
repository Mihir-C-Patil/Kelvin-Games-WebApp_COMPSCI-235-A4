const sidebar = document.querySelector(".sidebar");
const toggle = document.querySelector(".header__hamburger");
const topLine = document.querySelector(".hamburger__top")
const middleLine = document.querySelector(".hamburger__middle")
const bottomLine = document.querySelector(".hamburger__bottom")
const overlay = document.querySelector(".overlay")

toggle.addEventListener('click', () => {
    const visible = sidebar.getAttribute('data-visible');
    if (visible === "false") {
        sidebar.setAttribute('data-visible', true);
        topLine.classList.add("rotate")
        middleLine.classList.add("hide")
        bottomLine.classList.add("rotate-minus")
        overlay.classList.remove("hide")
    } else {
        sidebar.setAttribute('data-visible', false);
        topLine.classList.remove("rotate")
        middleLine.classList.remove("hide")
        bottomLine.classList.remove("rotate-minus")
        overlay.classList.add("hide")
    }
})