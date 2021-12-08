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
        form.appendChild(hiddenField1);
    document.body.appendChild(form);
    form.submit();	
};

function fieldlessPost(api) {
    var form = document.createElement('form');
    form.setAttribute('method', 'post'); 
    form.setAttribute('action', '/api/' + api);	
    form.setAttribute('target', 'iframe1');	
    document.charset = "utf-8";
    document.body.appendChild(form);
    form.submit();	
}

function getPir() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/pir', true);
    xhr.responseType='json';
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send();
    xhr.onload = function () {
        if (xhr.status == 200) {
            console.log(xhr.response);
            document.getElementById("pir").innerHTML = xhr.response.result;
            console.log("통신 성공");
        } else {
            document.getElementById("pir").innerHTML = "ERROR";
            console.log("통신 실패");
        }
    }
}

function musicAjax(pause, next) {
    var xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/music', true);
        xhr.responseType='json';
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.send(`pause=${pause}&next=${next}`);
        xhr.onload = function () {
            if (xhr.status == 200) {
                console.log(xhr.response);
                console.log("통신 성공");
            } else {
                console.log("통신 실패");
            }
        }
}

window.onload = function() {
    pir = setInterval(getPir, 1000);
}