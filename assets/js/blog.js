/**
 * Blog Filter, Search, and Reading Progress Script
 * Handles real-time category filtering, title search on blog.html,
 * and reading progress bar & Table of Contents highlighting on single blog posts.
 */

document.addEventListener('DOMContentLoaded', () => {
  initBlogFilters();
  initReadingProgress();
});

/**
 * Category Filtering & Instant Search for blog.html
 */
function initBlogFilters() {
  const filterButtons = document.querySelectorAll('.blog-filter-btn');
  const blogCards = document.querySelectorAll('.blog-card');
  const searchInput = document.getElementById('blog-search-input');
  const noResults = document.getElementById('blog-no-results');

  if (!filterButtons.length || !blogCards.length) return;

  let currentCategory = 'all';
  let searchQuery = '';

  function filterPosts() {
    let visibleCount = 0;

    blogCards.forEach(card => {
      const categories = card.dataset.categories ? card.dataset.categories.toLowerCase() : '';
      const title = card.querySelector('h2, h3') ? card.querySelector('h2, h3').textContent.toLowerCase() : '';
      const excerpt = card.querySelector('p') ? card.querySelector('p').textContent.toLowerCase() : '';

      const matchesCategory = currentCategory === 'all' || categories.includes(currentCategory);
      const matchesSearch = !searchQuery || title.includes(searchQuery) || excerpt.includes(searchQuery);

      if (matchesCategory && matchesSearch) {
        card.style.display = 'flex';
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.style.display = 'none';
        card.classList.add('hidden');
      }
    });

    if (noResults) {
      if (visibleCount === 0) {
        noResults.classList.remove('hidden');
      } else {
        noResults.classList.add('hidden');
      }
    }
  }

  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      filterButtons.forEach(b => {
        b.classList.remove('bg-emerald-600', 'text-white', 'border-emerald-600');
        b.classList.add('bg-white', 'dark:bg-slate-800', 'text-slate-700', 'dark:text-slate-300', 'border-slate-200', 'dark:border-slate-700');
        b.setAttribute('aria-pressed', 'false');
      });

      btn.classList.remove('bg-white', 'dark:bg-slate-800', 'text-slate-700', 'dark:text-slate-300', 'border-slate-200', 'dark:border-slate-700');
      btn.classList.add('bg-emerald-600', 'text-white', 'border-emerald-600');
      btn.setAttribute('aria-pressed', 'true');

      currentCategory = btn.dataset.category ? btn.dataset.category.toLowerCase() : 'all';
      filterPosts();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.toLowerCase().trim();
      filterPosts();
    });
  }
}

/**
 * Reading Progress Indicator & Sticky Table of Contents for Single Blog Posts
 */
function initReadingProgress() {
  const progressBar = document.getElementById('reading-progress-bar');
  const article = document.querySelector('article');

  if (progressBar && article) {
    window.addEventListener('scroll', () => {
      const totalHeight = article.clientHeight - window.innerHeight;
      const progress = Math.max(0, Math.min(100, (window.scrollY / totalHeight) * 100));
      progressBar.style.width = `${progress}%`;
    });
  }

  // Table of Contents Highlight
  const tocLinks = document.querySelectorAll('.toc-link');
  const headings = document.querySelectorAll('article h2[id], article h3[id]');

  if (tocLinks.length && headings.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          tocLinks.forEach(link => {
            if (link.getAttribute('href') === `#${id}`) {
              link.classList.add('text-emerald-600', 'dark:text-emerald-400', 'font-bold');
              link.classList.remove('text-slate-600', 'dark:text-slate-400');
            } else {
              link.classList.remove('text-emerald-600', 'dark:text-emerald-400', 'font-bold');
              link.classList.add('text-slate-600', 'dark:text-slate-400');
            }
          });
        }
      });
    }, { rootMargin: '0px 0px -60% 0px' });

    headings.forEach(heading => observer.observe(heading));
  }
}
