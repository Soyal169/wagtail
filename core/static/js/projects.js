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
        b.classList.remove('bg-emerald-600', 'text-white', 'border-emerald-600');
        b.classList.add('bg-white', 'dark:bg-slate-800', 'text-slate-700', 'dark:text-slate-300', 'border-slate-200', 'dark:border-slate-700');
        b.setAttribute('aria-pressed', 'false');
      });

      btn.classList.remove('bg-white', 'dark:bg-slate-800', 'text-slate-700', 'dark:text-slate-300', 'border-slate-200', 'dark:border-slate-700');
      btn.classList.add('bg-emerald-600', 'text-white', 'border-emerald-600');
      btn.setAttribute('aria-pressed', 'true');

      let visibleCount = 0;

      // Filter projects
      projectCards.forEach(card => {
        const cardCategories = card.getAttribute('data-categories') || '';
        if (category === 'all' || cardCategories.includes(category)) {
          card.classList.remove('hidden');
          visibleCount++;
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

      const noResults = document.getElementById('projects-no-results');
      if (noResults) {
        if (visibleCount === 0) {
          noResults.classList.remove('hidden');
        } else {
          noResults.classList.add('hidden');
        }
      }
    });
  });

  const resetBtn = document.querySelector('.reset-projects-filter');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      const allBtn = document.querySelector('.filter-btn[data-category="all"]');
      if (allBtn) allBtn.click();
    });
  }
});
