/* =========================================================
   WANDERWELL
   MAIN JAVASCRIPT
========================================================= */

document.addEventListener("DOMContentLoaded", function () {


    /* =====================================================
       FAQ ACCORDION
    ====================================================== */

    const faqQuestions = document.querySelectorAll(".faq-question");

    faqQuestions.forEach(function (question) {

        question.addEventListener("click", function () {

            const faqItem = this.closest(".faq-item");
            const isOpen = faqItem.classList.contains("active");

            // Close all other FAQ items
            document.querySelectorAll(".faq-item").forEach(function (item) {

                item.classList.remove("active");

                const itemQuestion = item.querySelector(".faq-question");

                if (itemQuestion) {
                    itemQuestion.setAttribute(
                        "aria-expanded",
                        "false"
                    );
                }

            });


            // Open the clicked item if it was closed
            if (!isOpen) {

                faqItem.classList.add("active");

                this.setAttribute(
                    "aria-expanded",
                    "true"
                );

            }

        });

    });


    /* =====================================================
       NAVIGATION - CLOSE MOBILE MENU AFTER CLICK
    ====================================================== */

    const navLinks = document.querySelectorAll(
        ".navbar-nav .nav-link"
    );

    const navigationMenu = document.querySelector(
        "#mainNavigation"
    );


    navLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            // Only close the menu on smaller screens
            if (window.innerWidth < 992 && navigationMenu) {

                const bootstrapCollapse =
                    bootstrap.Collapse.getInstance(
                        navigationMenu
                    );

                if (bootstrapCollapse) {
                    bootstrapCollapse.hide();
                }

            }

        });

    });


    /* =====================================================
       SMOOTH SCROLLING
    ====================================================== */

    const smoothLinks = document.querySelectorAll(
        'a[href^="#"]'
    );

    smoothLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const targetId = this.getAttribute("href");

            if (
                targetId &&
                targetId !== "#" &&
                document.querySelector(targetId)
            ) {

                event.preventDefault();

                const target =
                    document.querySelector(targetId);

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }

        });

    });


    /* =====================================================
       IMAGE LOADING EFFECT
    ====================================================== */

    const images = document.querySelectorAll("img");

    images.forEach(function (image) {

        if (image.complete) {
            image.classList.add("loaded");
        } else {

            image.addEventListener("load", function () {
                image.classList.add("loaded");
            });

        }

    });


    /* =====================================================
       SCROLL REVEAL
    ====================================================== */

    const revealElements = document.querySelectorAll(
        ".destination-card, " +
        ".tour-card, " +
        ".why-card, " +
        ".faq-item"
    );


    if ("IntersectionObserver" in window) {

        const revealObserver =
            new IntersectionObserver(
                function (entries, observer) {

                    entries.forEach(function (entry) {

                        if (entry.isIntersecting) {

                            entry.target.classList.add(
                                "reveal-visible"
                            );

                            observer.unobserve(
                                entry.target
                            );

                        }

                    });

                },
                {
                    threshold: 0.12
                }
            );


        revealElements.forEach(function (element) {

            element.classList.add("reveal-hidden");

            revealObserver.observe(element);

        });

    } else {

        revealElements.forEach(function (element) {
            element.classList.add("reveal-visible");
        });

    }


    /* =====================================================
       CURRENT YEAR
    ====================================================== */

    const currentYear =
        document.querySelector(".current-year");

    if (currentYear) {
        currentYear.textContent =
            new Date().getFullYear();
    }

});