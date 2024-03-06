const faqQuestions = document.querySelectorAll('.faq-question');

faqQuestions.forEach(question => {
    question.addEventListener('click', function () {
        const answer = this.nextElementSibling;
        answer.classList.toggle('show');
        // const arrow = this.querySelector('.faq-arrow');
        // arrow.classList.toggle('rotate'); // Simplified class toggle
    });
});