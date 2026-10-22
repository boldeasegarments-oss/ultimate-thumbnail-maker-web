/**
 * Interactive Cutout Studio Simulator Widget.
 * Accurately simulates the 5 cutout modes from activity_eraser.xml:
 * - Auto (0 to 80 threshold seekbar, default 52)
 * - Lasso (0 to 300 offset seekbar with Cut Inside/Outside)
 * - Erase (0 to 300 offset seekbar for fingertip elevation)
 * - Restore (1 to 40 radius brush)
 * - Zoom (100% to 400% magnification)
 */
function initCutoutInteractiveStudio() {
  const studio = document.getElementById('cutout-interactive-studio');
  if (!studio) return;

  const slider = studio.querySelector('#cutout-threshold-range');
  const valDisplay = studio.querySelector('#cutout-threshold-val');
  const labelDisplay = studio.querySelector('#cutout-slider-label');
  const modePills = studio.querySelectorAll('.ark-mode-pill');
  const badge = studio.querySelector('#cutout-status-badge');
  const desc = studio.querySelector('#cutout-mode-info');
  const cutoutPhone = document.querySelector('.ark-section-cutout .ark-phone');

  const modeData = {
    auto: {
      badge: 'Auto Color Erase',
      label: 'Threshold Tolerance',
      min: 0,
      max: 80,
      defaultVal: 52,
      unit: '',
      desc: '<strong>Auto Color Erase:</strong> 1-tap instant color backdrop clearing. Adjust threshold (0 to 80) to clean edges around clothing and hair without manual tracing.'
    },
    lasso: {
      badge: 'Polygon Lasso Active',
      label: 'Path Offset',
      min: 0,
      max: 300,
      defaultVal: 150,
      unit: ' px',
      desc: '<strong>Lasso Mode:</strong> Draw freehand custom boundaries around your subject with dedicated Cut Inside and Cut Outside buttons for rapid subject isolation.'
    },
    erase: {
      badge: 'Manual Offset Eraser',
      label: 'Fingertip Offset',
      min: 0,
      max: 300,
      defaultVal: 150,
      unit: ' px',
      desc: '<strong>Manual Erase:</strong> Elevated cursor offsets the eraser point (0 to 300px) above your fingertip so your touch never blocks the cutting boundary.'
    },
    restore: {
      badge: 'Precision Paint-Back',
      label: 'Brush Radius',
      min: 1,
      max: 40,
      defaultVal: 20,
      unit: ' px',
      desc: '<strong>Restore Mode:</strong> Accidental over-erase? Switch to restore mode and brush back original subject pixels without restarting from scratch.'
    },
    zoom: {
      badge: 'Sub-Pixel Inspection',
      label: 'Canvas Magnification',
      min: 100,
      max: 400,
      defaultVal: 250,
      unit: '%',
      desc: '<strong>Zoom Mode:</strong> Pinch & pan up to 400% to inspect sub-pixel boundaries and fine hair strands with razor-sharp clarity.'
    }
  };

  let currentMode = 'auto';

  function updateSliderVisual(val) {
    if (!slider || !valDisplay) return;
    const data = modeData[currentMode] || modeData.auto;
    valDisplay.textContent = `${val}${data.unit}`;
    const min = Number(slider.min) || 0;
    const max = Number(slider.max) || 80;
    const pct = max > min ? ((val - min) / (max - min)) * 100 : 50;
    slider.style.background = `linear-gradient(to right, #047857 0%, #047857 ${pct}%, #E2E8F0 ${pct}%, #E2E8F0 100%)`;
    if (cutoutPhone) {
      cutoutPhone.style.setProperty('--cutout-glow', `${(val / (max || 1)).toFixed(2)}`);
    }
  }

  // Live Slider Input
  if (slider && valDisplay) {
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

      currentMode = modeKey;
      if (badge) badge.textContent = data.badge;
      if (desc) desc.innerHTML = data.desc;
      if (labelDisplay) labelDisplay.textContent = data.label;

      if (slider && valDisplay) {
        slider.min = data.min;
        slider.max = data.max;
        slider.value = data.defaultVal;
        updateSliderVisual(slider.value);
      }
    });
  });
}

/**
 * Mobile Navigation Drawer Controller.
 */
function initMobileNav() {
  const toggle = document.querySelector('.mobile-toggle');
  const menu = document.getElementById('nav-menu');
  if (!toggle || !menu) return;

  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    toggle.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
  });

  document.addEventListener('click', (e) => {
    if (menu.classList.contains('is-open') && !menu.contains(e.target) && !toggle.contains(e.target)) {
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open navigation menu');
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && menu.classList.contains('is-open')) {
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open navigation menu');
    }
  });
}

/**
 * Header Scroll Appearance.
 */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const onScroll = () => {
    if (window.scrollY > 20) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/**
 * Global App Initialization.
 */

/**
 * HD Thumbnail Showcase Gallery (Interactive Category & Thumbnail Selector).
 */
function initHDGallery() {
  const card = document.getElementById('hd-gallery-card');
  if (!card) return;

  const tabBtns = card.querySelectorAll('.ark-tab-btn');
  const stripItems = card.querySelectorAll('.ark-strip-item');
  const activeImg = card.querySelector('#gallery-active-img');
  const stageBadge = card.querySelector('.ark-stage-badge');

  if (!tabBtns.length || !stripItems.length || !activeImg) return;

  function selectByIndex(targetIndex) {
    const idx = parseInt(targetIndex, 10);
    if (isNaN(idx)) return;

    // 1. Update Category Filter Pills
    tabBtns.forEach((btn) => {
      const bIdx = parseInt(btn.getAttribute('data-index'), 10);
      const isMatch = bIdx === idx;
      btn.classList.toggle('is-active', isMatch);
      btn.setAttribute('aria-selected', isMatch ? 'true' : 'false');
      if (isMatch) {
        btn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    });

    // 2. Update Thumbnail Strip Previews
    stripItems.forEach((item) => {
      const sIdx = parseInt(item.getAttribute('data-index'), 10);
      const isMatch = sIdx === idx;
      item.classList.toggle('is-active', isMatch);
      item.setAttribute('aria-selected', isMatch ? 'true' : 'false');
    });

    // 3. Update Featured 16:9 Display Stage
    const activeTab = Array.from(tabBtns).find(b => parseInt(b.getAttribute('data-index'), 10) === idx) || tabBtns[0];
    if (activeTab) {
      const src = activeTab.getAttribute('data-src');
      const title = activeTab.getAttribute('data-title') || activeTab.textContent.trim();
      
      activeImg.style.opacity = '0.35';
      activeImg.style.transform = 'scale(0.985)';
      
      const newImg = new Image();
      newImg.onload = () => {
        activeImg.src = src;
        activeImg.alt = title + ' - Full HD 1280x720 YouTube Thumbnail export preview ready for YouTube Studio';
        activeImg.style.opacity = '1';
        activeImg.style.transform = 'scale(1)';
      };
      newImg.src = src;

      if (stageBadge) {
        stageBadge.textContent = '1280 × 720 HD';
      }
    }
  }

  // Click on Tab Buttons
  tabBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const idx = btn.getAttribute('data-index');
      selectByIndex(idx);
    });
  });

  // Click on Strip Thumbnails
  stripItems.forEach((item) => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const idx = item.getAttribute('data-index');
      selectByIndex(idx);
    });
  });

  // Click on the main stage image advances to next thumbnail
  if (activeImg && activeImg.parentElement) {
    activeImg.parentElement.style.cursor = 'pointer';
    activeImg.parentElement.addEventListener('click', () => {
      const currentActive = card.querySelector('.ark-tab-btn.is-active');
      const currentIdx = currentActive ? parseInt(currentActive.getAttribute('data-index'), 10) : 0;
      const nextIdx = (currentIdx + 1) % tabBtns.length;
      selectByIndex(nextIdx);
    });
  }
}

/**
 * Interactive 3D Thumbnail Studio Sandbox Controller.
 */
function initThumbnailStudio() {
  const studio = document.getElementById('thumbnail-studio');
  if (!studio) return;

  const genreBtns = studio.querySelectorAll('.studio-tab-btn');
  const headlineInput = studio.querySelector('#studio-headline-input');
  const styleBtns = studio.querySelectorAll('.studio-pill-btn');
  const toggle3dBtn = studio.querySelector('#btn-toggle-3d');
  
  const canvas = studio.querySelector('.studio-canvas');
  const headline = studio.querySelector('.studio-headline');
  const badgeTag = studio.querySelector('.studio-badge-tag');
  const bgLayer = studio.querySelector('.studio-layer--bg');

  const presets = {
    gaming: {
      headline: 'EPIC BOSS DEFEATED!',
      tag: '100% UNLOCKED',
      tagBg: '#E11D48',
      textColor: '#FFEA00',
      bgGrad: 'linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%)'
    },
    youtube: {
      headline: 'I SPENT 24 HOURS HERE',
      tag: 'VIRAL VLOG',
      tagBg: '#DC2626',
      textColor: '#FFFFFF',
      bgGrad: 'linear-gradient(135deg, #451a03 0%, #1e1b4b 100%)'
    },
    tech: {
      headline: 'DO NOT BUY THIS YET',
      tag: 'BRUTAL TRUTH',
      tagBg: '#2563EB',
      textColor: '#38BDF8',
      bgGrad: 'linear-gradient(135deg, #09090b 0%, #172554 100%)'
    },
    tutorial: {
      headline: 'EDIT LIKE A PRO IN 10M',
      tag: 'MASTERCLASS',
      tagBg: '#059669',
      textColor: '#34D399',
      bgGrad: 'linear-gradient(135deg, #064e3b 0%, #0f172a 100%)'
    }
  };

  // 1. Genre Switching
  genreBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      genreBtns.forEach((b) => {
        b.classList.remove('is-active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('is-active');
      btn.setAttribute('aria-selected', 'true');

      const theme = btn.getAttribute('data-theme') || 'gaming';
      const preset = presets[theme];
      if (!preset) return;

      if (headline) {
        headline.textContent = preset.headline;
        headline.style.color = preset.textColor;
      }
      if (headlineInput) {
        headlineInput.value = preset.headline;
      }
      if (badgeTag) {
        badgeTag.textContent = preset.tag;
        badgeTag.style.background = preset.tagBg;
      }
      if (bgLayer) {
        bgLayer.style.background = preset.bgGrad;
      }
    });
  });

  // 2. Real-time Headline Input
  if (headlineInput && headline) {
    headlineInput.addEventListener('input', (e) => {
      headline.textContent = e.target.value.trim() || 'YOUR TITLE HERE';
    });
  }

  // 3. Font / Letter Styling Pills
  styleBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      styleBtns.forEach((b) => b.classList.remove('is-active'));
      btn.classList.add('is-active');

      const styleKey = btn.getAttribute('data-style') || 'impact';
      if (headline) {
        headline.classList.remove('style-impact', 'style-italic', 'style-cyber');
        headline.classList.add('style-' + styleKey);
      }
    });
  });

  // 4. 3D Exploded View Toggle
  if (toggle3dBtn && canvas) {
    toggle3dBtn.addEventListener('click', () => {
      const isExploded = canvas.classList.toggle('is-exploded');
      const textSpan = toggle3dBtn.querySelector('span');
      if (textSpan) {
        textSpan.textContent = isExploded ? 'Reset Flat View' : 'Toggle 3D Exploded View';
      }
      toggle3dBtn.classList.toggle('is-active', isExploded);
    });
  }
}

function initApp() {
  initHDGallery();
  initThumbnailStudio();
  initCutoutInteractiveStudio();
  initMobileNav();
  initHeaderScroll();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
