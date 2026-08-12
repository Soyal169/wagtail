/**
 * Main Application JS
 * Handles Theme Engine (Dark / Light)
 * Detects device system preference (Light vs Dark) on first visit,
 * and allows user to toggle and save their preferred theme.
 */

(function () {
  'use strict';

  function getInitialTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light' || savedTheme === 'dark') {
      return savedTheme;
    }
    // If no saved theme, detect device/browser system preference
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
      root.classList.remove('light');
    } else {
      root.classList.remove('dark');
      root.classList.add('light');
    }

    updateToggleButtons(theme);
  }

  function updateToggleButtons(theme) {
    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    if (!toggleBtns.length) return;

    const nextThemeLabel = theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme';
    toggleBtns.forEach(btn => {
      btn.setAttribute('aria-label', nextThemeLabel);
      btn.setAttribute('title', nextThemeLabel);
    });
  }

  // Execute theme check immediately to prevent flashing
  const currentTheme = getInitialTheme();
  applyTheme(currentTheme);

  document.addEventListener('DOMContentLoaded', () => {
    updateToggleButtons(getInitialTheme());
    initThemeToggle();
    updateCopyrightYear();
  });

  function initThemeToggle() {
    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    if (!toggleBtns.length) return;

    toggleBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const isCurrentlyDark = document.documentElement.classList.contains('dark');
        const nextTheme = isCurrentlyDark ? 'light' : 'dark';

        applyTheme(nextTheme);
        localStorage.setItem('theme', nextTheme);
      });
    });
  }

  function updateCopyrightYear() {
    const yearEls = document.querySelectorAll('.current-year');
    const currentYear = new Date().getFullYear();
    yearEls.forEach(el => {
      el.textContent = currentYear;
    });
  }
})();
