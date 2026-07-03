(function () {
  function retryImage(img) {
    if (img.dataset.retryAttempted === "true") {
      return;
    }

    img.dataset.retryAttempted = "true";
    var source = img.currentSrc || img.getAttribute("src");
    if (!source) {
      return;
    }

    var url = new URL(source, window.location.href);
    url.searchParams.set("retry", Date.now().toString());

    window.setTimeout(function () {
      img.src = url.href;
    }, 400);
  }

  function initMediaRetry() {
    document.querySelectorAll("img").forEach(function (img) {
      img.addEventListener("error", function () {
        retryImage(img);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMediaRetry);
  } else {
    initMediaRetry();
  }
})();
