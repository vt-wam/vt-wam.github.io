(function () {
  function getTabs() {
    return Array.prototype.slice.call(document.querySelectorAll('.comparison-tab'));
  }

  function getPanels() {
    return Array.prototype.slice.call(document.querySelectorAll('.comparison-panel'));
  }

  function stopPanelVideos(panel) {
    panel.querySelectorAll('video').forEach(function (video) {
      try {
        video.pause();
        if (video.readyState > 0) {
          video.currentTime = 0;
        }
      } catch (error) {
        // Some browsers reject seeking before metadata is loaded.
      }
    });
  }

  function activatePanel(targetId) {
    if (!targetId) {
      return;
    }

    getTabs().forEach(function (tab) {
      var isActive = tab.getAttribute('data-demo-target') === targetId;
      tab.classList.toggle('is-active', isActive);
      tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
      tab.tabIndex = isActive ? 0 : -1;
    });

    getPanels().forEach(function (panel) {
      var isActive = panel.id === targetId;
      panel.classList.toggle('is-active', isActive);
      panel.hidden = !isActive;
      panel.toggleAttribute('hidden', !isActive);

      if (!isActive) {
        stopPanelVideos(panel);
      }
    });
  }

  function initComparisonTabs() {
    var activeTab = document.querySelector('.comparison-tab.is-active') || document.querySelector('.comparison-tab');
    if (activeTab) {
      activatePanel(activeTab.getAttribute('data-demo-target'));
    }
  }

  document.addEventListener('click', function (event) {
    var tab = event.target.closest('.comparison-tab');
    if (!tab) {
      return;
    }

    event.preventDefault();
    activatePanel(tab.getAttribute('data-demo-target'));
  });

  document.addEventListener('keydown', function (event) {
    var tab = event.target.closest('.comparison-tab');
    if (!tab || (event.key !== 'Enter' && event.key !== ' ')) {
      return;
    }

    event.preventDefault();
    activatePanel(tab.getAttribute('data-demo-target'));
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initComparisonTabs);
  } else {
    initComparisonTabs();
  }
})();

