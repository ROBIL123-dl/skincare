document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('vendorRegistrationForm');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');
    const togglePassword = document.getElementById('togglePassword');
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');

    // Function to toggle password visibility
    function togglePasswordVisibility(inputField, toggleIcon) {
        toggleIcon.addEventListener('click', function() {
            const type = inputField.getAttribute('type') === 'password' ? 'text' : 'password';
            inputField.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }

    // Toggle password visibility for both password fields
    togglePasswordVisibility(password, togglePassword);
    togglePasswordVisibility(confirmPassword, toggleConfirmPassword);

    // Form validation
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        } else {
            event.preventDefault(); // Prevent actual form submission for this example
            alert('Form submitted successfully!');
            form.reset();
        }

        form.classList.add('was-validated');
    }, false);

    // Custom validation for password match
    confirmPassword.addEventListener('input', function() {
        if (password.value !== confirmPassword.value) {
            confirmPassword.setCustomValidity("Passwords do not match");
        } else {
            confirmPassword.setCustomValidity("");
        }
    });

    // Custom validation for password strength
    password.addEventListener('input', function() {
        if (password.value.length < 8) {
            password.setCustomValidity("Password must be at least 8 characters long");
        } else {
            password.setCustomValidity("");
        }
    });

    // Custom validation for file type
    const license = document.getElementById('license');
    license.addEventListener('change', function() {
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'];
        if (this.files.length > 0 && !allowedTypes.includes(this.files[0].type)) {
            this.setCustomValidity("Please upload a PDF, JPEG, or PNG file");
        } else {
            this.setCustomValidity("");
        }
    });
});