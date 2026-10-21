/**
 * Ultimate Thumbnail Maker - Main Client Script
 * Accessible Mobile Navigation & Outbound Analytics Tracker
 * 
 * Note: Core website functionality and text content remain 100% accessible
 * even if JavaScript is disabled.
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initPlayStoreTracking();
  initCurrentYear();
});

/**
 * Mobile navigation menu toggle with ARIA attributes and keyboard management.
 */
function initMobileNav() {
  const toggleBtn = document.querySelector('.mobile-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (!toggleBtn || !navMenu) return;

  function toggleMenu(open) {
    const isCurrentlyOpen = navMenu.classList.contains('is-open');
    const newState = typeof open === 'boolean' ? open : !isCurrentlyOpen;

    navMenu.classList.toggle('is-open', newState);
    toggleBtn.setAttribute('aria-expanded', String(newState));
    toggleBtn.setAttribute('aria-label', newState ? 'Close navigation menu' : 'Open navigation menu');

    // Update hamburger icon visual
    const icon = toggleBtn.querySelector('svg');
    if (icon) {
      if (newState) {
        // Render Close (X) icon
        icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />';
      } else {
        // Render Hamburger icon
        icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
      }
    }
  }

  toggleBtn.addEventListener('click', () => {
    toggleMenu();
  });

  // Close menu on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navMenu.classList.contains('is-open')) {
      toggleMenu(false);
      toggleBtn.focus();
    }
  });

  // Close menu when clicking outside
  document.addEventListener('click', (e) => {
    if (navMenu.classList.contains('is-open') &&
        !navMenu.contains(e.target) &&
        !toggleBtn.contains(e.target)) {
      toggleMenu(false);
    }
  });

  // Close menu when clicking a navigation link
  navMenu.querySelectorAll('.nav-link').forEach((link) => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 768) {
        toggleMenu(false);
      }
    });
  });
}

/**
 * Privacy-friendly outbound Google Play click tracker.
 * Checks for configured analytics (gtag or dataLayer) without throwing errors.
 * Never prevents or delays destination link navigation.
 */
function initPlayStoreTracking() {
  const ctaLinks = document.querySelectorAll('.js-play-store-cta');

  ctaLinks.forEach((link) => {
    link.addEventListener('click', (event) => {
      const sourcePage = link.getAttribute('data-source-page') || 'unknown';
      const destination = link.getAttribute('href') || '';

      // Optional Google Analytics 4 tracking (safe execution)
      if (typeof window.gtag === 'function') {
        try {
          window.gtag('event', 'play_store_click', {
            event_category: 'outbound',
            event_label: sourcePage,
            destination_url: destination,
            transport_type: 'beacon'
          });
        } catch (err) {
          // Fail silently to prevent user navigation interruption
        }
      } else if (Array.isArray(window.dataLayer)) {
        // Support custom GTM dataLayer
        try {
          window.dataLayer.push({
            event: 'play_store_click',
            sourcePage: sourcePage,
            destinationUrl: destination
          });
        } catch (err) {
          // Fail silently
        }
      }

      // Note: We do not call event.preventDefault() so standard browser
      // navigation always proceeds immediately and reliably.
    });
  });
}

/**
 * Updates dynamic copyright year in footer.
 */
function initCurrentYear() {
  const yearElement = document.getElementById('current-year');
  if (yearElement) {
    yearElement.textContent = String(new Date().getFullYear());
  }
}
