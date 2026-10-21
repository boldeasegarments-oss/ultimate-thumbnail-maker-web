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
  initHero3DParallax();
  initCursorGlowTracker();
  initScrollReveal();
  initThumbnailStudio();
  initCompareSlider();
  initCutoutInteractiveStudio();
  initHDThumbnailGallery();
  initExportSimulator();
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

      const x = (clientX - bounds.left) / bounds.width - 0.5;
      const y = (clientY - bounds.top) / bounds.height - 0.5;

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

    card.addEventListener('touchstart', onMouseEnter, { passive: true });
    card.addEventListener('touchmove', onMouseMove, { passive: true });
    card.addEventListener('touchend', onMouseLeave, { passive: true });
  });
}

/**
 * Modern 3D Parallax & Gyroscope Cursor Tracking for Ark7 Hero Duo Phones.
 * Smoothly tilts the front phone and shifts the back phone in complementary 3D space.
 */
function initHero3DParallax() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  const heroSection = document.querySelector('.ark-hero');
  const frontPhone = document.querySelector('.ark-phone--front');
  const backPhone = document.querySelector('.ark-phone--back');
  if (!heroSection || !frontPhone) return;

  let currentX = 0, currentY = 0;
  let targetX = 0, targetY = 0;
  let isRunning = false;

  function render() {
    currentX += (targetX - currentX) * 0.08;
    currentY += (targetY - currentY) * 0.08;

    const rotX = (-currentY * 8).toFixed(2);
    const rotY = (currentX * 10).toFixed(2);

    frontPhone.style.transform = `perspective(1200px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale3d(1.02, 1.02, 1.02)`;

    if (backPhone) {
      const backRotX = (-currentY * 4).toFixed(2);
      const backRotY = (currentX * 5).toFixed(2);
      const backOffsetX = (-currentX * 15).toFixed(1);
      const backOffsetY = (-currentY * 12).toFixed(1);
      backPhone.style.transform = `rotate(-7deg) translate3d(${backOffsetX}px, ${backOffsetY}px, 0) scale(0.92) perspective(1200px) rotateX(${backRotX}deg) rotateY(${backRotY}deg)`;
    }

    if (Math.abs(targetX - currentX) > 0.001 || Math.abs(targetY - currentY) > 0.001) {
      requestAnimationFrame(render);
    } else {
      isRunning = false;
    }
  }

  function startRender() {
    if (!isRunning) {
      isRunning = true;
      requestAnimationFrame(render);
    }
  }

  heroSection.addEventListener('mousemove', (e) => {
    const rect = heroSection.getBoundingClientRect();
    targetX = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
    targetY = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
    startRender();
  });

  heroSection.addEventListener('mouseleave', () => {
    targetX = 0;
    targetY = 0;
    startRender();
  });

  // Mobile gyroscope tilt
  if (window.DeviceOrientationEvent && window.matchMedia('(hover: none)').matches) {
    window.addEventListener('deviceorientation', (e) => {
      if (e.gamma === null || e.beta === null) return;
      targetX = Math.max(-1, Math.min(1, e.gamma / 30));
      targetY = Math.max(-1, Math.min(1, (e.beta - 45) / 30));
      startRender();
    }, { passive: true });
  }
}

/**
 * Interactive 3D Thumbnail Studio Sandbox.
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
  const categoryTabs = studioRoot.querySelectorAll('.studio-tab-btn');
  const stylePills = studioRoot.querySelectorAll('.studio-pill-btn');

  const themes = {
    gaming: {
      headline: 'EPIC BOSS DEFEATED!',
      badge: '100% UNLOCKED',
      badgeColor: '#EF4444',
      bgImage: "url('/assets/templates/studio-bg-gaming.webp')",
      textColor: '#FFEA00',
      textShadow: '3px 3px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 0 8px 25px rgba(255, 234, 0, 0.5)'
    },
    youtube: {
      headline: 'I LOST EVERYTHING HERE',
      badge: 'SECRET LOCATION',
      badgeColor: '#E11D48',
      bgImage: "url('/assets/templates/studio-bg-vlog.webp')",
      textColor: '#FFFFFF',
      textShadow: '3px 3px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 0 8px 25px rgba(0, 0, 0, 0.85)'
    },
    tech: {
      headline: "DON'T BUY THIS YET!",
      badge: 'THE BRUTAL TRUTH',
      badgeColor: '#0284C7',
      bgImage: "url('/assets/templates/studio-bg-tech.webp')",
      textColor: '#38BDF8',
      textShadow: '3px 3px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 0 8px 25px rgba(56, 189, 248, 0.6)'
    },
    tutorial: {
      headline: 'THIS CHANGES EVERYTHING',
      badge: 'MASTERCLASS 2026',
      badgeColor: '#8B5CF6',
      bgImage: "url('/assets/templates/studio-bg-tutorial.webp')",
      textColor: '#FCD34D',
      textShadow: '3px 3px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 0 8px 25px rgba(252, 211, 77, 0.6)'
    }
  };

  if (layerBg) {
    layerBg.style.backgroundImage = themes.gaming.bgImage;
    layerBg.style.backgroundSize = 'cover';
    layerBg.style.backgroundPosition = 'center';
  }

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

  if (textInput && headlineEl) {
    textInput.addEventListener('input', (e) => {
      const val = e.target.value.trim();
      headlineEl.textContent = val.length > 0 ? val : 'YOUR TITLE HERE';
    });
  }

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

  if (toggle3DBtn && canvas) {
    toggle3DBtn.addEventListener('click', () => {
      canvas.classList.toggle('is-exploded');
    });
  }
}

/**
 * Draggable Before / After Cutout Comparison Slider.
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
      const clamped = Math.max(0.05, Math.min(0.95, rawPos));
      const percentage = (clamped * 100).toFixed(2);

      afterWrap.style.width = `${percentage}%`;
      handle.style.left = `${percentage}%`;
      slider.style.setProperty('--clip-pos', `${percentage}%`);
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
      slider.style.setProperty('--clip-pos', `${newVal}%`);
      slider.setAttribute('aria-valuenow', String(newVal));
    });
  });
}

/**
 * Interactive Cursor Spotlight Glow Tracking.
 */
function initCursorGlowTracker() {
  const cards = document.querySelectorAll('.bento-card, .review-card, .template-card, .ark-phone');
  if (!cards.length) return;

  cards.forEach((card) => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });
}

/**
 * Modern Staggered Scroll Reveal Animations.
 */
function initScrollReveal() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  const revealElements = document.querySelectorAll('.bento-card, .template-card, .review-card, .step-item, .ark-story-content, .ark-story-media-wrap');
  if (!revealElements.length || !('IntersectionObserver' in window)) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-revealed');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  });

  revealElements.forEach((el, index) => {
    el.classList.add('reveal-on-scroll');
    el.style.setProperty('--reveal-delay', `${(index % 4) * 0.1}s`);
    observer.observe(el);
  });
}

/**
 * Interactive Background Eraser Studio Widget.
 * Connects the range slider to live threshold values, updates mode pills and descriptions.
 */
function initCutoutInteractiveStudio() {
  const studio = document.getElementById('cutout-interactive-studio');
  if (!studio) return;

  const slider = studio.querySelector('#cutout-threshold-range');
  const valDisplay = studio.querySelector('#cutout-threshold-val');
  const modePills = studio.querySelectorAll('.ark-mode-pill');
  const badge = studio.querySelector('#cutout-status-badge');
  const desc = studio.querySelector('#cutout-mode-info');
  const cutoutPhone = document.querySelector('.ark-section-cutout .ark-phone');

  const modeData = {
    auto: {
      badge: '0.2s Auto Isolation',
      desc: '⚡ <strong>Auto Mode:</strong> 1-tap instant color backdrop clearing with neural edge refine.',
      defaultVal: 70
    },
    lasso: {
      badge: 'Polygon Lasso Active',
      desc: '✂ <strong>Lasso Mode:</strong> Trace freehand custom boundaries to cut inside or outside the polygon.',
      defaultVal: 85
    },
    brush: {
      badge: 'Offset Brush (30px)',
      desc: '🎯 <strong>Manual Brush:</strong> Fine-tune fine hair strands with fingertip offset cursor guidance.',
      defaultVal: 45
    },
    restore: {
      badge: 'Smart Paint-Back',
      desc: '↺ <strong>Restore Mode:</strong> Bring back accidentally erased subject details without restarting.',
      defaultVal: 50
    },
    zoom: {
      badge: 'Pixel Precision 400%',
      desc: '🔍 <strong>Zoom Mode:</strong> Pinch & pan to inspect sub-pixel boundaries in razor-sharp detail.',
      defaultVal: 100
    }
  };

  // Live Slider Input
  if (slider && valDisplay) {
    function updateSliderVisual(val) {
      valDisplay.textContent = `${val}%`;
      const pct = ((val - slider.min) / (slider.max - slider.min)) * 100;
      slider.style.background = `linear-gradient(to right, var(--ark-green) 0%, var(--ark-green) ${pct}%, #CBD5E1 ${pct}%, #CBD5E1 100%)`;
      if (cutoutPhone) {
        cutoutPhone.style.setProperty('--cutout-glow', `${(val / 70).toFixed(2)}`);
      }
    }

    slider.addEventListener('input', (e) => {
      updateSliderVisual(e.target.value);
    });

    updateSliderVisual(slider.value);
  }

  // Mode Buttons
  modePills.forEach((btn) => {
    btn.addEventListener('click', () => {
      modePills.forEach((p) => {
        p.classList.remove('is-active');
        p.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('is-active');
      btn.setAttribute('aria-selected', 'true');

      const modeKey = btn.getAttribute('data-mode') || 'auto';
      const data = modeData[modeKey];
      if (!data) return;

      if (badge) badge.textContent = data.badge;
      if (desc) desc.innerHTML = data.desc;
      if (slider && valDisplay) {
        slider.value = data.defaultVal;
        slider.dispatchEvent(new Event('input'));
      }
    });
  });
}

/**
 * Clean & Minimalist HD Thumbnail Gallery in Section 5 (Export in Full HD).
 * Synchronizes category filter tabs, featured 16:9 stage, and visual thumbnail strip.
 */
function initHDThumbnailGallery() {
  const card = document.getElementById('hd-gallery-card');
  if (!card) return;

  const tabs = card.querySelectorAll('.ark-tab-btn');
  const stripItems = card.querySelectorAll('.ark-strip-item');
  const stageImg = document.getElementById('gallery-active-img');

  function setActive(index) {
    tabs.forEach((tab, i) => {
      const isActive = i === index;
      tab.classList.toggle('is-active', isActive);
      tab.setAttribute('aria-selected', String(isActive));
    });

    stripItems.forEach((item, i) => {
      const isActive = i === index;
      item.classList.toggle('is-active', isActive);
      item.setAttribute('aria-selected', String(isActive));
    });

    const activeTab = tabs[index];
    if (stageImg && activeTab) {
      const src = activeTab.getAttribute('data-src');
      const title = activeTab.getAttribute('data-title') || 'Thumbnail';
      stageImg.style.opacity = '0.35';
      stageImg.style.transform = 'scale(0.985)';
      setTimeout(() => {
        stageImg.src = src;
        stageImg.alt = `${title} - Full HD 1280x720 YouTube Thumbnail export preview`;
        stageImg.style.opacity = '1';
        stageImg.style.transform = 'scale(1)';
      }, 120);
    }
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => setActive(index));
  });

  stripItems.forEach((item, index) => {
    item.addEventListener('click', () => setActive(index));
  });
}

/**
 * Interactive Export Simulator Widget in Section 5.
 * Allows creators to test 1-tap export presets and experience instant YouTube Studio readiness.
 */
function initExportSimulator() {
  const card = document.getElementById('export-interactive-card');
  if (!card) return;

  const presets = card.querySelectorAll('.ark-preset-btn');
  const resTag = card.querySelector('#export-res-tag');
  const testBtn = card.querySelector('#btn-test-export');
  const feedback = card.querySelector('#export-status-feedback');

  const presetData = {
    yt: { res: '1280 × 720 HD', status: 'Ready: 1280×720 • Zero Compression • PNG (16:9)' },
    shorts: { res: '1080 × 1920 4K', status: 'Ready: 1080×1920 • YouTube Shorts / Reels (9:16)' },
    post: { res: '1080 × 1080 HD', status: 'Ready: 1080×1080 • Square Community Post (1:1)' }
  };

  presets.forEach((btn) => {
    btn.addEventListener('click', () => {
      presets.forEach((p) => p.classList.remove('is-active'));
      btn.classList.add('is-active');

      const key = btn.getAttribute('data-preset') || 'yt';
      const data = presetData[key];
      if (!data) return;

      if (resTag) resTag.textContent = data.res;
      if (feedback) {
        feedback.textContent = data.status;
        feedback.classList.remove('is-active');
      }
    });
  });

  if (testBtn) {
    let isExporting = false;
    testBtn.addEventListener('click', () => {
      if (isExporting) return;
      isExporting = true;

      const originalHtml = testBtn.innerHTML;
      testBtn.innerHTML = '<span>⚡ Exporting in Full HD...</span>';
      testBtn.style.opacity = '0.85';

      setTimeout(() => {
        testBtn.innerHTML = '<span>✓ Saved to Gallery (0.2s)</span>';
        testBtn.classList.add('is-success');
        testBtn.style.opacity = '1';

        if (feedback) {
          feedback.textContent = '✓ 1280×720 300 DPI PNG Saved • Ready for YouTube Studio!';
          feedback.classList.add('is-active');
        }

        setTimeout(() => {
          testBtn.innerHTML = originalHtml;
          testBtn.classList.remove('is-success');
          isExporting = false;
        }, 2800);
      }, 350);
    });
  }
}
