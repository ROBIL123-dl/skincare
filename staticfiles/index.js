const scrollContainer = document.querySelector('.scroll-container');
const scrollLeft = document.getElementById('scrollLeft');
const scrollRight = document.getElementById('scrollRight');
const testimonials = [
    {
        image: "https://via.placeholder.com/80",
        text: "This service is amazing! I couldn't be happier.",
        name: "John Doe"
    },
    {
        image: "https://via.placeholder.com/80",
        text: "Absolutely fantastic support and results.",
        name: "Jane Smith"
    },
    {
        image: "https://via.placeholder.com/80",
        text: "Highly recommend to anyone looking for quality!",
        name: "Alice Johnson"
    },
    {
        image: "https://via.placeholder.com/80",
        text: "The experience was beyond my expectations!",
        name: "Robert Brown"
    }
];
let currentIndex = 0;

function updateTestimonial() {
    const testimonial = testimonials[currentIndex];
    scrollContainer.innerHTML = `
        <div class="scroll-item">
            <div class="testimonial-card card text-center p-3">
                <img src="${testimonial.image}" alt="Client ${currentIndex + 1}" class="testimonial-img mx-auto">
                <p class="testimonial-text">"${testimonial.text}"</p>
                <p class="testimonial-name fw-bold">- ${testimonial.name}</p>
            </div>
        </div>
    `;
}

scrollLeft.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
    updateTestimonial();
});

scrollRight.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % testimonials.length;
    updateTestimonial();
});

// Initialize the first testimonial
updateTestimonial();