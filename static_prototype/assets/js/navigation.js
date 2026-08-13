/**
 * Navigation JS
 * Accessible Mobile Drawer, Sticky Header, & Active Link Highlighting
 * Supports relative, root-relative, and file protocol pathing seamlessly.
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  const header = document.querySelector('header');
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const navLinks = document.querySelectorAll('nav a');

  // Sticky Header elevation on scroll
  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 20) {
        header.classList.add('shadow-md', 'backdrop-blur-md', 'bg-opacity-90');
      } else {
        header.classList.remove('shadow-md', 'backdrop-blur-md', 'bg-opacity-90');
      }
    }, { passive: true });
  }

  // Mobile Menu Drawer Toggle & Accessibility
  if (mobileMenuBtn && mobileMenu) {
    let isOpen = false;

    const toggleMenu = (open) => {
      isOpen = typeof open === 'boolean' ? open : !isOpen;
      mobileMenuBtn.setAttribute('aria-expanded', isOpen.toString());
      
      if (isOpen) {
        mobileMenu.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
      } else {
        mobileMenu.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
      }
    };

    mobileMenuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleMenu();
    });

    // Close mobile menu on Escape key press
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && isOpen) {
        toggleMenu(false);
        mobileMenuBtn.focus();
      }
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (isOpen && !mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
        toggleMenu(false);
      }
    });
  }

  // Active Link Highlighting
  const rawPath = window.location.pathname;
  // Get filename or default to index.html
  const currentFilename = rawPath.split('/').pop() || 'index.html';

  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;
    
    // Extract target filename from href
    const targetFilename = href.split('#')[0].split('/').pop() || 'index.html';

    const isMatch = (currentFilename === targetFilename) ||
                    (currentFilename === '' && targetFilename === 'index.html') ||
                    (currentFilename === 'index.html' && targetFilename === 'index.html');

    if (isMatch) {
      link.classList.add('text-emerald-500', 'font-semibold');
      link.setAttribute('aria-current', 'page');
    } else {
      link.setAttribute('aria-current', 'false');
    }
  });
});
