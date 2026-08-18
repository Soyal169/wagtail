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
    initCopyButtons();
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

  function initCopyButtons() {
    document.querySelectorAll('.copy-terminal-btn').forEach(btn => {
      btn.addEventListener('click', async () => {
        const terminalWindow = btn.closest('.terminal-window');
        if (!terminalWindow) return;
        const rows = terminalWindow.querySelectorAll('.terminal-body div');
        const text = Array.from(rows).map(r => r.innerText).join('\n');
        try {
          await navigator.clipboard.writeText('{\n  ' + text.split('\n').join('\n  ') + '\n}');
          showCopiedFeedback(btn);
        } catch (e) {
          // Fallback
          showCopiedFeedback(btn);
        }
      });
    });

    document.querySelectorAll('.copy-code-btn').forEach(btn => {
      btn.addEventListener('click', async () => {
        const container = btn.closest('.code-block-container') || btn.parentElement.parentElement;
        if (!container) return;
        const codeElem = container.querySelector('.pygments-code') || container.querySelector('pre') || container.querySelector('code');
        if (!codeElem) return;
        try {
          await navigator.clipboard.writeText(codeElem.innerText);
          showCopiedFeedback(btn);
        } catch (e) {
          showCopiedFeedback(btn);
        }
      });
    });
  }

  function showCopiedFeedback(btn) {
    const textSpan = btn.querySelector('.btn-text');
    const originalText = textSpan ? textSpan.textContent : 'copy';
    btn.classList.add('text-emerald-500', 'dark:text-emerald-400');
    if (textSpan) textSpan.textContent = 'copied!';
    setTimeout(() => {
      btn.classList.remove('text-emerald-500', 'dark:text-emerald-400');
      if (textSpan) textSpan.textContent = originalText;
    }, 2000);
  }

  function updateCopyrightYear() {
    const yearEls = document.querySelectorAll('.current-year');
    const currentYear = new Date().getFullYear();
    yearEls.forEach(el => {
      el.textContent = currentYear;
    });
  }
})();
