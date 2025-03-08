window.onscroll = function() {shrinkHeader()};
google.charts.load("current", {packages:["corechart"]});
google.charts.setOnLoadCallback(drawChart);

function shrinkHeader() {
    const header = document.getElementById("main-header");
    const mainContent = document.getElementById("main-content");

    if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
        header.classList.add("small");
        mainContent.classList.add("header-small");
    } else {
        header.classList.remove("small");
        mainContent.classList.remove("header-small");
    }
}

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}