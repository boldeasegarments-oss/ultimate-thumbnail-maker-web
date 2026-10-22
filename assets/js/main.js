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
function initApp() {
  initCutoutInteractiveStudio();
  initMobileNav();
  initHeaderScroll();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
