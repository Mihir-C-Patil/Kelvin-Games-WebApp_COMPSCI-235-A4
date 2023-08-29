const sidebar = document.querySelector(".sidebar");
const toggle = document.querySelector(".header__hamburger");
const topLine = document.querySelector(".hamburger__top");
const middleLine = document.querySelector(".hamburger__middle");
const bottomLine = document.querySelector(".hamburger__bottom");
const overlay = document.querySelector(".overlay");
const hoverThreshold = 20;

toggle.addEventListener('click', () => {
    toggleSidebar();
});

overlay.addEventListener('click', () => {
    toggleSidebar();
});

document.addEventListener('mousemove', (event) => {
    const mouseX = event.clientX;

    if (mouseX <= hoverThreshold) {
        openSidebar();
    }
});

function openSidebar() {
    sidebar.setAttribute('data-visible', true);
    topLine.classList.add("rotate");
    middleLine.classList.add("hide");
    bottomLine.classList.add("rotate-minus");
    overlay.classList.remove("hide");
}

function closeSidebar() {
    sidebar.setAttribute('data-visible', false);
    topLine.classList.remove("rotate");
    middleLine.classList.remove("hide");
    bottomLine.classList.remove("rotate-minus");
    overlay.classList.add("hide");
}

function toggleSidebar() {
    const visible = sidebar.getAttribute('data-visible');
    if (visible === "false") {
        openSidebar();
    } else {
        closeSidebar();
    }
}
