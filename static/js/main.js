function led(led) { //1~4 : 각각, 0 : 전부 끄기, 5 : 전부 켜기
    console.log(led);
    var form = document.createElement('form');
    form.setAttribute('method', 'post'); 
    form.setAttribute('action', '/api/led');	
    form.setAttribute('target', 'iframe1');	
    document.charset = "utf-8";
        var hiddenField1 = document.createElement('input');
        hiddenField1.setAttribute('type', 'hidden'); 
        hiddenField1.setAttribute('name', "led");
        hiddenField1.setAttribute('value', led);
    document.body.appendChild(form);
    form.submit();	
};


var fan = function() {
    var currentFan = document.getElementById("fan").textContent;
    var form = document.createElement('form');
    form.setAttribute('method', 'post'); 
    form.setAttribute('action', '/api/fan');	
    form.setAttribute('target', 'iframe1');	
    document.charset = "utf-8";
        var hiddenField1 = document.createElement('input');
        hiddenField1.setAttribute('type', 'hidden'); 
        hiddenField1.setAttribute('name', "fan");
        hiddenField1.setAttribute('value', currentFan);
    document.body.appendChild(form);
    form.submit();	
};
document.addEventListener("DOMContentLoaded", function() {
    var startbtn = document.getElementById("btn-fan");
    startbtn.addEventListener("click",fan);
});