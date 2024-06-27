let sidebar=document.querySelector(".side-bar");
console.log(sidebar)
let sidebarBtn=document.getElementsByClassName("sidebarBtn");
console.log(sidebarBtn);
for(let i=0;i<sidebarBtn.length;i++){
    sidebarBtn[i].addEventListener("click",()=>{
        sidebar.classList.toggle("active");
        console.log("hi");
    });
}


$(window).on('load', function() {
   $('#loader').addClass('hidden');
  $('form').submit(function() {
    $('#loader').removeClass('hidden');
  });
});


