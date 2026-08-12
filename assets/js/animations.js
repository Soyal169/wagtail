/**
 * Scroll Reveal Animations using IntersectionObserver
 * Performance-optimized, non-blocking UI effects
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) return;

  const revealElements = document.querySelectorAll('.reveal-on-scroll');
  if (!revealElements.length) return;

  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -50px 0px',
    threshold: 0.15
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        obs.unobserve(entry.target); // Unobserve once revealed for better performance
      }
    });
  }, observerOptions);

  revealElements.forEach(el => observer.observe(el));
});
