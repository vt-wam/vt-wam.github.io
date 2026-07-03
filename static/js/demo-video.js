(function () {
  function showSeekWarning() {
    var warning = document.getElementById("demo-video-seek-warning");
    if (warning) {
      warning.hidden = false;
    }
  }

  function initDemoVideo() {
    var video = document.getElementById("demo-video");
    if (!video) {
      return;
    }

    video.controls = true;
    video.preload = "metadata";
    video.playsInline = true;
    video.setAttribute("controlsList", "nodownload");

    video.addEventListener("contextmenu", function (event) {
      event.preventDefault();
    });

    if (location.protocol === "file:") {
      showSeekWarning();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initDemoVideo);
  } else {
    initDemoVideo();
  }
})();
