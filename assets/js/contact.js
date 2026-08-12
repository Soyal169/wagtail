/**
 * Contact Form Validation & Interactive Utilities
 * Prepared for future Django POST submission with zero accidental page reloads
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  // Contact Form Handling
  const contactForm = document.getElementById('portfolio-contact-form');
  const formFeedback = document.getElementById('form-feedback');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      // If no valid backend POST URL is specified, prevent browser reload/redirect
      const action = contactForm.getAttribute('action');
      if (!action || action === '' || action === '#' || action === 'index.html') {
        e.preventDefault();
      }

      const nameInput = document.getElementById('form-name');
      const emailInput = document.getElementById('form-email');
      const messageInput = document.getElementById('form-message');

      let isValid = true;

      // Simple validation
      [nameInput, emailInput, messageInput].forEach(input => {
        if (input && !input.value.trim()) {
          isValid = false;
          input.classList.add('border-red-500');
          input.setAttribute('aria-invalid', 'true');
        } else if (input) {
          input.classList.remove('border-red-500');
          input.setAttribute('aria-invalid', 'false');
        }
      });

      if (!isValid) {
        e.preventDefault();
        if (formFeedback) {
          formFeedback.textContent = 'Please fill out all required fields correctly.';
          formFeedback.className = 'mt-4 p-3 rounded-lg bg-red-900/40 text-red-300 border border-red-800 text-sm font-medium';
          formFeedback.classList.remove('hidden');
        }
        return;
      }

      // If static prototype, prevent submit & display confirmation message
      if (!action || action === '' || action === '#') {
        e.preventDefault();
        if (formFeedback) {
          formFeedback.textContent = 'Thank you! Your message has been prepared. In production, this submits directly to the Django backend handler.';
          formFeedback.className = 'mt-4 p-3 rounded-lg bg-emerald-900/40 text-emerald-300 border border-emerald-800 text-sm font-medium';
          formFeedback.classList.remove('hidden');
        }
        contactForm.reset();
      }
    });
  }

  // Copy Email Button Utility
  const copyBtns = document.querySelectorAll('.copy-email-btn');
  copyBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const email = btn.getAttribute('data-email') || 'soyal@example.com';
      navigator.clipboard.writeText(email).then(() => {
        const originalText = btn.textContent;
        btn.textContent = 'Copied to Clipboard!';
        btn.classList.add('bg-emerald-600', 'text-white');
        setTimeout(() => {
          btn.textContent = originalText;
          btn.classList.remove('bg-emerald-600', 'text-white');
        }, 2000);
      }).catch(err => {
        console.error('Failed to copy email:', err);
      });
    });
  });
});
