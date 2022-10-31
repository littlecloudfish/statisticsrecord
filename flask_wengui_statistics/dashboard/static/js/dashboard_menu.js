function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }

  function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

  function checkCookie() {
    let user = getCookie("username");
    if (user != "") {
      alert("Welcome again " + user);
    } else {
      user = prompt("Please enter your name:", "");
      if (user != "" && user != null) {
        setCookie("username", user, 365);
      }
    }
  }

  function setSidebar() {
    sidebar = document.getElementsByClassName('sidebar')[0];
    homeSection = document.getElementsByClassName('home')[0];

    var menu_cookie = getCookie('menu_status');
    if (menu_cookie == "") {
      setCookie('menu_status', 'open', 30);
    }

    if (menu_cookie == 'close') {
      sidebar.classList.add("close");
      homeSection.classList.add("close");
    } else {
      sidebar.classList.remove("close")
      homeSection.classList.remove("close");
    }
};

// document.addEventListener('DOMContentLoaded', () => {
//   sidebar = document.getElementsByClassName('sidebar')[0];
//   // homeSection = document.getElementsByClassName('home')[0];

//   var menu = getCookie('menu_status');
//   if (menu == "") {
//     setCookie('menu_status', 'open', 30);
//   }

//   if (menu == 'close') {
//     sidebar.classList.add("close");
//   } else {
//     sidebar.classList.remove("close")
//   }
// });

window.addEventListener('DOMContentLoaded', setSidebar);

jQuery(function () {
  const body = document.querySelector('body'),
    sidebar = body.querySelector('nav'),
    //   sidebar_debug = body.querySelector('.sidebar_debug'),
    toggle = body.querySelector(".toggle"),
    // toggle_debug = body.querySelector(".toggle_debug"),
    searchBtn = body.querySelector(".search"),
    // // modeSwitch = body.querySelector(".toggle-switch"),
    // modeText = body.querySelector(".mode-text"),
    // // NM
    // sideBar = body.querySelector(".sidebar"),
    // navLink = body.querySelector(".nav-link"),
    homeSection = body.querySelector(".home");


    toggle.addEventListener("click", (ev) => {
      sidebar.classList.toggle("close");
      homeSection.classList.toggle("close");

      if (sidebar.classList.contains("close")) {
        setCookie('menu_status', 'close', 30);
        homeSection.style.setProperty('left', '78px');
        homeSection.style.setProperty('width', 'calc(100% - 78px)');
      }
      else {
        setCookie('menu_status', 'open', 30);
        homeSection.style.setProperty('left', '250px');
        homeSection.style.setProperty('width', 'calc(100% - 250px)');
      }

      ev.stopPropagation();
    });

  window.addEventListener('load', homeWidth);

 function homeWidth() {
    var menu = getCookie('menu_status');

   if (menu == 'close') {
      homeSection.style.setProperty('left', '78px');
      homeSection.style.setProperty('width', 'calc(100% - 78px)');

    } else {
      homeSection.style.setProperty('left', '250px');
      homeSection.style.setProperty('width', 'calc(100% - 250px)');
    }
  };

  function homeAdjust() {
    var widthHome = 0;
    var boolSideBarLeft = sidebar.classList.contains("close");
    //   var boolSideBarRight = sidebar_debug.classList.contains("close");

    if (boolSideBarLeft) {
      widthHome += 78;
      homeSection.style.setProperty('left', '78px');
    }
    else {
      widthHome += 250;
      homeSection.style.setProperty('left', '250px');
    }

    //   if (boolSideBarRight) {
    //       widthHome += 78;
    //       homeSection.style.setProperty('right', '78px');
    //   }
    //   else {
    //   widthHome += 250;
    //   homeSection.style.setProperty('right', '250px');
    //   }

    if (widthHome == 78)
      homeSection.style.setProperty('width', 'calc(100% - 78px)');
    //   else if (widthHome == 156)
    //       homeSection.style.setProperty('width', 'calc(100% - 156px)');
    //   else if (widthHome == 328)
    //       homeSection.style.setProperty('width', 'calc(100% - 328px)');
    else
      homeSection.style.setProperty('width', 'calc(100% - 250px)');
  };

  searchBtn.addEventListener("click", (ev) => {
    sidebar.classList.remove("close");
    // NM
    ev.stopPropagation();
  });



  // modeSwitch.addEventListener("click", () => {
  //   body.classList.toggle("dark");

  //   if (body.classList.contains("dark")) {
  //     modeText.innerText = "Light mode";
  //   } else {
  //     modeText.innerText = "Dark mode";
  //   }
  // });
});

// $(function () {
//   // Iterate over each select element
//   $('select').each(function () {

//       // Cache the number of options
//       var $this = $(this),
//           numberOfOptions = $(this).children('option').length;

//       // Hides the select element
//       $this.addClass('s-hidden');

//       // Wrap the select element in a div
//       $this.wrap('<div class="select"></div>');

//       // Insert a styled div to sit over the top of the hidden select element
//       $this.after('<div class="styledSelect"></div>');

//       // Cache the styled div
//       var $styledSelect = $this.next('div.styledSelect');

//       // Show the first select option in the styled div
//       $styledSelect.text($this.children('option').eq(0).text());

//       // Insert an unordered list after the styled div and also cache the list
//       var $list = $('<ul />', {
//           'class': 'options'
//       }).insertAfter($styledSelect);

//       // Insert a list item into the unordered list for each select option
//       for (var i = 0; i < numberOfOptions; i++) {
//           $('<li />', {
//               text: $this.children('option').eq(i).text(),
//               rel: $this.children('option').eq(i).val()
//           }).appendTo($list);
//       }

//       // Cache the list items
//       var $listItems = $list.children('li');

//       // Show the unordered list when the styled div is clicked (also hides it if the div is clicked again)
//       $styledSelect.on("click",function (e) {
//           e.stopPropagation();
//           $('div.styledSelect.active').each(function () {
//               $(this).removeClass('active').next('ul.options').hide();
//           });
//           $(this).toggleClass('active').next('ul.options').toggle();
//       });

//       // Hides the unordered list when a list item is clicked and updates the styled div to show the selected list item
//       // Updates the select element to have the value of the equivalent option
//       $listItems.on("click",function (e) {
//           e.stopPropagation();
//           $styledSelect.text($(this).text()).removeClass('active');
//           $this.val($(this).attr('rel'));
//           $list.hide();
//           /* alert($this.val()); Uncomment this for demonstration! */
//       });

//       // Hides the unordered list when clicking outside of it
//       $(document).on("click",function () {
//           $styledSelect.removeClass('active');
//           $list.hide();
//       });
//   });
// });