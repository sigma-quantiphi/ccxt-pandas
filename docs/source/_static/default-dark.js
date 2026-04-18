// Force dark mode on first visit; respect user toggle once they pick one.
(function () {
  if (!localStorage.getItem("theme")) {
    document.body.dataset.theme = "dark";
    localStorage.setItem("theme", "dark");
  }
})();
