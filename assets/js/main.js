/**
 * Ultimate Thumbnail Maker - Main Client Script
 * Accessible Mobile Navigation, Outbound Analytics Tracker,
 * Interactive 3D Perspective Tilt Physics,
 * Interactive 3D Thumbnail Studio Sandbox, and Before/After Cutout Slider.
 * 
 * Note: Core website functionality and text content remain 100% accessible
 * even if JavaScript is disabled.
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initPlayStoreTracking();
  initCurrentYear();
  init3DTilt();
  initThumbnailStudio();
  initCompareSlider();
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
    link.addEventListener('click', () => {
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

/**
 * Interactive 3D Perspective Tilt Physics with Dynamic Specular Glare.
 * Attaches to any element with .card-3d or [data-tilt].
 */
function init3DTilt() {
  // Respect user preference for reduced motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  const cards = document.querySelectorAll('.card-3d, [data-tilt]');
  if (!cards.length) return;

  cards.forEach((card) => {
    const glare = card.querySelector('.card-3d-glare');
    const maxTilt = parseFloat(card.getAttribute('data-tilt-max') || '12');

    let isHovered = false;
    let bounds = null;

    function onMouseEnter() {
      isHovered = true;
      bounds = card.getBoundingClientRect();
      if (glare) {
        glare.style.setProperty('--glare-opacity', '1');
      }
    }

    function onMouseMove(e) {
      if (!isHovered) {
        bounds = card.getBoundingClientRect();
        isHovered = true;
      }
      if (!bounds) return;

      const clientX = e.clientX || (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
      const clientY = e.clientY || (e.touches && e.touches[0] ? e.touches[0].clientY : 0);

      const x = (clientX - bounds.left) / bounds.width - 0.5; // -0.5 to 0.5
      const y = (clientY - bounds.top) / bounds.height - 0.5; // -0.5 to 0.5

      const rotateX = (-y * maxTilt).toFixed(2);
      const rotateY = (x * maxTilt).toFixed(2);

      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;

      if (glare) {
        const glareX = ((x + 0.5) * 100).toFixed(1);
        const glareY = ((y + 0.5) * 100).toFixed(1);
        glare.style.setProperty('--glare-x', `${glareX}%`);
        glare.style.setProperty('--glare-y', `${glareY}%`);
        glare.style.setProperty('--glare-opacity', '1');
      }
    }

    function onMouseLeave() {
      isHovered = false;
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      if (glare) {
        glare.style.setProperty('--glare-opacity', '0');
      }
    }

    card.addEventListener('mouseenter', onMouseEnter);
    card.addEventListener('mousemove', onMouseMove);
    card.addEventListener('mouseleave', onMouseLeave);

    // Support passive touch on mobile
    card.addEventListener('touchstart', onMouseEnter, { passive: true });
    card.addEventListener('touchmove', onMouseMove, { passive: true });
    card.addEventListener('touchend', onMouseLeave, { passive: true });
  });
}

/**
 * Interactive 3D Thumbnail Studio Sandbox.
 * Lets visitors test real creator workflows: swap category themes,
 * customize live headline text, switch fonts, and toggle 3D exploded layer view.
 */
function initThumbnailStudio() {
  const studioRoot = document.getElementById('thumbnail-studio');
  if (!studioRoot) return;

  const canvas = studioRoot.querySelector('.studio-canvas');
  const toggle3DBtn = studioRoot.querySelector('#btn-toggle-3d');
  const textInput = studioRoot.querySelector('#studio-headline-input');
  const headlineEl = studioRoot.querySelector('.studio-headline');
  const badgeEl = studioRoot.querySelector('.studio-badge-tag');
  const layerBg = studioRoot.querySelector('.studio-layer--bg');
  const subjectSilhouette = studioRoot.querySelector('.studio-subject-silhouette');
  const categoryTabs = studioRoot.querySelectorAll('.studio-tab-btn');
  const stylePills = studioRoot.querySelectorAll('.studio-pill-btn');

  // Preset themes configuration
  const themes = {
    gaming: {
      headline: 'EPIC BOSS DEFEATED!',
      badge: '100% UNLOCKED',
      badgeColor: '#ef4444',
      bgImage: "url('/assets/templates/gaming-hardcore.webp')",
      textColor: '#ffeb3b',
      textShadow: '3px 3px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 0 4px 18px rgba(255, 235, 59, 0.6)'
    },
    youtube: {
      headline: 'I SPENT 100 HOURS HERE',
      badge: 'VIRAL VLOG',
      badgeColor: '#e11d48',
      bgImage: "url('/assets/templates/vlog-travel.webp')",
      textColor: '#ffffff',
      textShadow: '3px 3px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 0 4px 18px rgba(244, 63, 94, 0.6)'
    },
    tech: {
      headline: "DON'T BUY THIS YET!",
      badge: 'ULTIMATE REVIEW',
      badgeColor: '#059669',
      bgImage: "url('/assets/templates/tech-review.webp')",
      textColor: '#34d399',
      textShadow: '3px 3px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 0 4px 18px rgba(52, 211, 153, 0.6)'
    },
    tutorial: {
      headline: 'PRO MASTERCLASS 2026',
      badge: 'STEP-BY-STEP',
      badgeColor: '#7c3aed',
      bgImage: "url('/assets/templates/pro-editor.webp')",
      textColor: '#f0abfc',
      textShadow: '3px 3px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 0 4px 18px rgba(192, 132, 252, 0.6)'
    }
  };

  // Set initial background image for gaming
  if (layerBg) {
    layerBg.style.backgroundImage = themes.gaming.bgImage;
    layerBg.style.backgroundSize = 'cover';
    layerBg.style.backgroundPosition = 'center';
  }

  // Switch category theme
  categoryTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      categoryTabs.forEach((t) => t.classList.remove('is-active'));
      tab.classList.add('is-active');

      const themeKey = tab.getAttribute('data-theme') || 'gaming';
      const theme = themes[themeKey];
      if (!theme) return;

      if (headlineEl) {
        headlineEl.textContent = theme.headline;
        headlineEl.style.color = theme.textColor;
        headlineEl.style.textShadow = theme.textShadow;
      }
      if (textInput) {
        textInput.value = theme.headline;
      }
      if (badgeEl) {
        badgeEl.textContent = theme.badge;
        badgeEl.style.backgroundColor = theme.badgeColor;
      }
      if (layerBg) {
        layerBg.style.backgroundImage = theme.bgImage;
        layerBg.style.backgroundSize = 'cover';
        layerBg.style.backgroundPosition = 'center';
      }
    });
  });

  // Headline real-time input handler
  if (textInput && headlineEl) {
    textInput.addEventListener('input', (e) => {
      const val = e.target.value.trim();
      headlineEl.textContent = val.length > 0 ? val : 'YOUR TITLE HERE';
    });
  }

  // Switch font style pills
  stylePills.forEach((pill) => {
    pill.addEventListener('click', () => {
      stylePills.forEach((p) => p.classList.remove('is-active'));
      pill.classList.add('is-active');

      const style = pill.getAttribute('data-style');
      if (!headlineEl) return;

      if (style === 'impact') {
        headlineEl.style.fontFamily = "'Bebas Neue', sans-serif";
        headlineEl.style.letterSpacing = '0.02em';
        headlineEl.style.textTransform = 'uppercase';
      } else if (style === 'italic') {
        headlineEl.style.fontFamily = "'The Bold Font', sans-serif";
        headlineEl.style.letterSpacing = '-0.01em';
        headlineEl.style.textTransform = 'uppercase';
      } else if (style === 'cyber') {
        headlineEl.style.fontFamily = "system-ui, sans-serif";
        headlineEl.style.letterSpacing = '0.05em';
        headlineEl.style.textTransform = 'uppercase';
      }
    });
  });
        headlineEl.style.textTransform = 'uppercase';
        headlineEl.style.fontStyle = 'normal';
      }
    });
  });

  // 3D Exploded Layer Mode Toggle
  if (toggle3DBtn && canvas) {
    toggle3DBtn.addEventListener('click', () => {
      const isExploded = canvas.classList.toggle('is-exploded');
      toggle3DBtn.classList.toggle('is-exploded-active', isExploded);

      const statusText = toggle3DBtn.querySelector('.btn-label-text');
      if (statusText) {
        statusText.textContent = isExploded ? 'Switch to Flat 2D Mode' : 'Toggle 3D Exploded View';
      }
    });
  }
}

/**
 * Draggable Before / After Cutout Comparison Slider.
 * Allows visitors to drag the slider handle with mouse or touch to see
 * raw background vs. clean background cutout side-by-side.
 */
function initCompareSlider() {
  const sliders = document.querySelectorAll('.compare-slider-wrap');
  if (!sliders.length) return;

  sliders.forEach((slider) => {
    const afterWrap = slider.querySelector('.compare-after-wrap');
    const handle = slider.querySelector('.compare-handle');
    if (!afterWrap || !handle) return;

    let isDragging = false;

    function updateSlider(clientX) {
      const rect = slider.getBoundingClientRect();
      const rawPos = (clientX - rect.left) / rect.width;
      // Clamp between 5% and 95%
      const clamped = Math.max(0.05, Math.min(0.95, rawPos));
      const percentage = (clamped * 100).toFixed(2);

      afterWrap.style.width = `${percentage}%`;
      handle.style.left = `${percentage}%`;
      slider.setAttribute('aria-valuenow', String(Math.round(clamped * 100)));
    }

    function onPointerDown(e) {
      isDragging = true;
      const clientX = e.clientX || (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
      updateSlider(clientX);
    }

    function onPointerMove(e) {
      if (!isDragging) return;
      const clientX = e.clientX || (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
      updateSlider(clientX);
    }

    function onPointerUp() {
      isDragging = false;
    }

    slider.addEventListener('mousedown', onPointerDown);
    window.addEventListener('mousemove', onPointerMove);
    window.addEventListener('mouseup', onPointerUp);

    slider.addEventListener('touchstart', onPointerDown, { passive: true });
    window.addEventListener('touchmove', onPointerMove, { passive: true });
    window.addEventListener('touchend', onPointerUp, { passive: true });

    // Keyboard accessibility: ArrowLeft / ArrowRight
    slider.addEventListener('keydown', (e) => {
      const currentVal = parseFloat(slider.getAttribute('aria-valuenow') || '50');
      let newVal = currentVal;
      if (e.key === 'ArrowLeft') {
        newVal = Math.max(5, currentVal - 5);
      } else if (e.key === 'ArrowRight') {
        newVal = Math.min(95, currentVal + 5);
      } else {
        return;
      }
      e.preventDefault();
      afterWrap.style.width = `${newVal}%`;
      handle.style.left = `${newVal}%`;
      slider.setAttribute('aria-valuenow', String(newVal));
    });
  });
}
