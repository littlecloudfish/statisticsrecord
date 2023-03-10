jQuery(function () {
  //   toggle.addEventListener("click", (ev) => {
  //   sidebar.classList.toggle("close");
  //   homeAdjust();

  //   ev.stopPropagation();
  // });

  const weight_sliders = document.getElementsByClassName('weight-slider');
  Array.from(weight_sliders).forEach((slider) => {
    slider.previousElementSibling.previousElementSibling.innerHTML = slider.value;
  });

  const weight_pres = ['mic', 'sim', 'ref', 'crt', 'rcd', 'ugt', 'cht'];
  Array.from(weight_pres).forEach((weight_pre) => {
    var total_weight = 0;
    const weights = document.getElementsByClassName('weight-' + weight_pre);
    Array.from(weights).forEach((weight) => {
      total_weight += Number(weight['value']);
    });
    document.getElementById(weight_pre + '_video').innerHTML = total_weight+'%';
  });
});

function weight_change(sender) {
  const weight_aera = sender['id'].substring(0, 3);
  sender.previousElementSibling.previousElementSibling.innerHTML = sender.value;

  var total_weight = 0;
  const weights = document.getElementsByClassName('weight-' + weight_aera);
  Array.from(weights).forEach((weight) => {
    total_weight += Number(weight['value']);
  });
  document.getElementById(weight_aera + '_video').innerHTML = total_weight + '%';
}
