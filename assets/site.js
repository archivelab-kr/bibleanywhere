// The only script: the language menu in the header goes to the same page in the chosen language.
document.querySelectorAll(".lang select").forEach(function (s) {
  s.addEventListener("change", function () { location.href = s.value; });
});
