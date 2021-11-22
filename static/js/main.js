var led = function() {
    var currentLed = document.getElementById("led").textContent;
    var form = document.createElement('form');
    form.setAttribute('method', 'post'); 
    form.setAttribute('action', '/api/led');	
    form.setAttribute('target', 'iframe1');	
    document.charset = "utf-8";
        var hiddenField1 = document.createElement('input');
        hiddenField1.setAttribute('type', 'hidden'); 
        hiddenField1.setAttribute('name', "led");
        hiddenField1.setAttribute('value', currentLed);
    document.body.appendChild(form);
    form.submit();	
};
document.addEventListener("DOMContentLoaded", function() {
    var startbtn = document.getElementById("btn_test");
    startbtn.addEventListener("click",led);
});