/**
 * Projects Filtering JS
 * Handles interactive filtering on projects.html without re-rendering HTML content
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');

  if (!filterBtns.length || !projectCards.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const category = btn.getAttribute('data-category');

      // Update button states
      filterBtns.forEach(b => {
        b.classList.remove('bg-emerald-500', 'text-white', 'border-emerald-500');
        b.classList.add('bg-slate-800', 'text-slate-300', 'border-slate-700', 'hover:border-slate-500');
        b.setAttribute('aria-pressed', 'false');
      });

      btn.classList.remove('bg-slate-800', 'text-slate-300', 'border-slate-700', 'hover:border-slate-500');
      btn.classList.add('bg-emerald-500', 'text-white', 'border-emerald-500');
      btn.setAttribute('aria-pressed', 'true');

      // Filter projects
      projectCards.forEach(card => {
        const cardCategories = card.getAttribute('data-categories') || '';
        if (category === 'all' || cardCategories.includes(category)) {
          card.classList.remove('hidden');
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
          }, 10);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'scale(0.95)';
          setTimeout(() => {
            card.classList.add('hidden');
          }, 200);
        }
      });
    });
  });
});
