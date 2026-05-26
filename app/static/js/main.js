window.addEventListener("load", function () {
    const menuBtn = document.getElementById("menu-btn");
    const mobileMenu = document.getElementById("mobile-menu");
    const menuOpenIcon = document.getElementById("menu-open-icon");
    const menuCloseIcon = document.getElementById("menu-close-icon");

    console.log("JS loaded");
    console.log("menuBtn:", menuBtn);
    console.log("mobileMenu:", mobileMenu);
    console.log("menuOpenIcon:", menuOpenIcon);
    console.log("menuCloseIcon:", menuCloseIcon);

    if (!menuBtn || !mobileMenu || !menuOpenIcon || !menuCloseIcon) {
        console.log("Navbar elements not found");
        return;
    }

    menuBtn.addEventListener("click", function () {
        console.log("Hamburger clicked");
        mobileMenu.classList.toggle("hidden");
        menuOpenIcon.classList.toggle("hidden");
        menuCloseIcon.classList.toggle("hidden");
    });
});