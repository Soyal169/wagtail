/**
 * Contact Form Validation & Interactive Utilities
 * Progressive-enhancement layer on top of the real Django form POST:
 * catches obviously-empty required fields before the round-trip, but the
 * server-side Django validation in ContactPage.serve() is always authoritative.
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  // Contact Form Handling
  const contactForm = document.getElementById('portfolio-contact-form');
  const formFeedback = document.getElementById('form-feedback');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
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
      }
      // If valid, let the form submit normally to the real Django view.
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
