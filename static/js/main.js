document.documentElement.className = document.documentElement.className.replace(
    "no-js",
    "js"
);
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.content [href^="#"]').forEach((link) => {
        link.addEventListener("click", (link) => {
            link.preventDefault(),
                document
                    .getElementById(link.getAttribute("href").substring(1))
                    .scrollIntoView({ behavior: "smooth" });
        });
    }),
        document.querySelectorAll('.content [href^="http"]').forEach((link) => {
            link.setAttribute("target", "_blank");
        });
});

document.addEventListener("DOMContentLoaded", function () {
    if (
        (document
            .getElementById("toggleTheme")
            .addEventListener("click", () => {
                if (
                    document.documentElement.getAttribute("data-bs-theme") ===
                    "dark"
                )
                    document.documentElement.setAttribute(
                        "data-bs-theme",
                        "light"
                    ),
                        (localStorage.theme = "light"),
                        (toggleTheme.innerHTML = "🌚");
                else
                    document.documentElement.setAttribute(
                        "data-bs-theme",
                        "dark"
                    ),
                        (localStorage.theme = "dark"),
                        (toggleTheme.innerHTML = "🌝");
            }),
        !("theme" in localStorage) ||
            document.documentElement.getAttribute("data-bs-theme", "dark") ||
            window.matchMedia("(prefers-color-scheme: auto)").matches)
    )
        localStorage.theme = "auto";
    if (
        localStorage.theme === "auto" ||
        (!("theme" in localStorage) &&
            window.matchMedia("(prefers-color-scheme: auto)").matches)
    )
        document.documentElement.setAttribute("data-bs-theme", "auto"),
            (localStorage.theme = "auto"),
            (document.getElementById("toggleTheme").innerHTML = "🌓");
    if (
        localStorage.theme === "dark" ||
        (!("theme" in localStorage) &&
            window.matchMedia("(prefers-color-scheme: dark)").matches)
    )
        document.documentElement.setAttribute("data-bs-theme", "dark"),
            (localStorage.theme = "dark"),
            (document.getElementById("toggleTheme").innerHTML = "🌝");
    if (
        localStorage.theme === "light" ||
        (!("theme" in localStorage) &&
            window.matchMedia("(prefers-color-scheme: light)").matches)
    )
        document.documentElement.setAttribute("data-bs-theme", "light"),
            (localStorage.theme = "light"),
            (document.getElementById("toggleTheme").innerHTML = "🌚");
});

//POPUP WINDOW PROTECTION
function openPopup(url, name, windowFeatures) {
    var newWindow = window.open(
        url,
        name,
        "noopener,noreferrer," + windowFeatures
    );
    newWindow.opener = null;
}

document.addEventListener("DOMContentLoaded", function () {
    // ANCHOR DEFAULT FUNCTION RESET
    document.querySelectorAll('.content [href="#"]').forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
        });
    });

    //BACK TO TOP
    let topButton = document.getElementById("btn-back-to-top");
    topButton.addEventListener("click", backToTop);

    function backToTop() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }
    window.onscroll = function () {
        scrollFunction();
    };

    function scrollFunction() {
        if (
            document.body.scrollTop > 20 ||
            document.documentElement.scrollTop > 20
        ) {
            topButton.style.display = "block";
        } else {
            topButton.style.display = "none";
        }
    }
    $(document).ready(function () {
        $("#btn-back-to-top").click(function () {
            $("html, body").animate({ scrollTop: 0 }, 300);
            return;
        });
    });
});

// LOADER ANIMATION
$(window).on("load", function () {
    $(".loader").delay(200).fadeOut("slow");
    $(".loader").addClass("active");
});

$(document).ready(function () {
    $(".navbar-toggler").click(function () {
        $("#navbarNav").slideToggle();
    });
});
