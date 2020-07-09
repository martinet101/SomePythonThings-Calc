async function checkUpdates() {
    let result = await eel.checkUpdates_py()();
    if(result === true){
        if (confirm("Found new updates. Do you want to download them?")){
            eel.downloadUpdates();
        }
    }
}

if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.write('<link id="style" rel="stylesheet" type="text/css" href="/style-dark.css"/>');
} else {
    document.write('<link id="style" rel="stylesheet" type="text/css" href="/style.css" title="light"/>');
}

function mode() {
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.getElementById('style').href = "style-dark.css";
    } else {
        document.getElementById('style').href = "style.css";
    }
}
checkUpdates();
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
    mode();
})

Mousetrap.bind('0', function () {
    if(canWrite){
        number(0);
    }
});

Mousetrap.bind('1', function () {
    if(canWrite){
        number(1);
    }
});

Mousetrap.bind('2', function () {
    if(canWrite){
        number(2);
    }
});

Mousetrap.bind('3', function () {
    if(canWrite){
        number(3);
    }
});

Mousetrap.bind('4', function () {
    if(canWrite){
        number(4);
    }
});

Mousetrap.bind('5', function () {
    if(canWrite){
        number(5);
    }
});

Mousetrap.bind('6', function () {
    if(canWrite){
        number(6);
    }
});

Mousetrap.bind('7', function () {
    if (canWrite){
    number(7);
    }
});

Mousetrap.bind('8', function () {
    if (canWrite){
    number(8);
    }
});

Mousetrap.bind('9', function () {
    if (canWrite){
    number(9);
    }
});

Mousetrap.bind('+', function () {
    if (canWrite){
    operation("+");
    }
});

Mousetrap.bind('-', function () {
    if (canWrite){
    operation("-");
    }
});

Mousetrap.bind('*', function () {
    if (canWrite){
    operation("*");
    }
});

Mousetrap.bind('/', function () {
    if (canWrite){
    operation("/");
    }
});

Mousetrap.bind('^', function () {
    if (canWrite){
    operation("**(");
    }
});

Mousetrap.bind('(', function () {
    if (canWrite){
    bracket("(");
    }
});

Mousetrap.bind(')', function () {
    if (canWrite){
    bracket(")");
    }
});

Mousetrap.bind('.', function () {
    if (canWrite){
    dot();
    }
});

Mousetrap.bind(',', function () {
    if (canWrite){
    dot();
    }
});

Mousetrap.bind('=', function () {
    if (canWrite){
    eval_js();
    }
});

Mousetrap.bind('enter', function () {
    if (canWrite){
    eval_js();
    }
});

Mousetrap.bind('backspace', function () {
    if (canWrite){
    del();
    }
});


function disableAll() {
    canWrite = false
    var x = document.getElementsByClassName("big");
    var i;
    for (i = 0; i < x.length; i++) {
        x[i].disabled = true;
        }
    var x = document.getElementsByClassName("small");
    var i;
    for (i = 0; i < x.length; i++) {
        x[i].disabled = true;
        }
    }

function enableAll() {
    canWrite = true
    var x = document.getElementsByClassName("small");
    var i;
    for (i = 0; i < x.length; i++) {
        x[i].disabled = false;
        }
    var x = document.getElementsByClassName("big");
    var i;
    for (i = 0; i < x.length; i++) {
        x[i].disabled = false;
        }
    }
var canWrite = true;
var operationAvailable = false;
var dotAvailable = true;
var bracketsToClose = 0;
var needClear = false;
var previousResult = 0;
var calcHistory = '';
var currentOperation = '';
var isPythonAlive = false;
var nul = ''

async function checkPython() {
    let result = await eel.python_alive()();
    isPythonAlive = result;
}

nul = checkPython();

async function eval_js() {
    if (true){
        startValue = document.getElementById('text').value
        console.log(currentOperation);
        if (eval(currentOperation) == 'Infinity'){
            if(confirm('The operation you entered seems to be very heavy. If you continue, Program may crash. Do you want to continue?')){
                disableAll();
                let result = await eel.py_eval(currentOperation)();
                enableAll();
                console.log(result);
                document.getElementById('text').value = startValue + "\n = " + result;
                console.log(typeof result);
                if (!(result.includes('Oh 💩, You did it again! The operation is too hard to be calculated!'))){
                    needClear = true;
                    previousResult = result;
                    dotAvailable = true;
                } else {
                    needClear = true;
                    dotAvailable = false;
                    operationAvailable = false;
                    bracketsToClose = 0;
                }
                console.log(calcHistory);
                calcHistory = document.getElementById('text').value;
                document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
            }
        } else {
            disableAll();
            let result = await eel.py_eval(currentOperation)();
            enableAll();
            console.log(result);
            document.getElementById('text').value = startValue + "\n = " + result;
            if (!(result.includes('Oh 💩, You did it again! The operation is too hard to be calculated!'))){
                needClear = true;
                dotAvailable = true;
                previousResult = result;
            } else {
                needClear = true;
                dotAvailable = false;
                operationAvailable = false;
                bracketsToClose = 0;
            }
            calcHistory = document.getElementById('text').value;
            document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
        }
    }
    if (previousResult == undefined) {
        alert("Connection lost with the python engine. Please restart the program. This may be because you entered a huge operation.");
    }
}

function number(n) {
    if (needClear === true) {
        document.getElementById('text').value = document.getElementById('text').value + "\n\n"
        needClear = false;
        currentOperation = '';
    }
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    document.getElementById('text').value = document.getElementById('text').value + n;
    currentOperation = currentOperation + n;
    operationAvailable = true;
}

function operation(o) {
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    if (needClear === true) {
        document.getElementById('text').value = document.getElementById('text').value + "\n\n" + previousResult;
        currentOperation = previousResult;
        needClear = false;
    }
    if ("**(/".includes(o)) {
        if (operationAvailable === true) {
            document.getElementById('text').value = document.getElementById('text').value + ' ' + o + ' ';
            currentOperation = currentOperation +  ' ' + o + ' ';
        }
    } else {
        document.getElementById('text').value = document.getElementById('text').value + ' ' + o + ' ';
        currentOperation = currentOperation + ' ' + o + ' ';
    }
    operationAvailable = false;
    dotAvailable = true;
    if (o === "**(") {
        bracketsToClose = bracketsToClose + 1;
    }
}

function bracket(b) {
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    operationAvailable = false;
    if (b === ")") {
        if (bracketsToClose > 0) {
            document.getElementById('text').value = document.getElementById('text').value + ' ' + b + ' ';
            currentOperation = currentOperation + ' '+ b + ' ' ;
            bracketsToClose = bracketsToClose - 1;
        }
    } else {
        bracketsToClose = bracketsToClose + 1;
        document.getElementById('text').value = document.getElementById('text').value + ' ' + b + ' ';
        currentOperation = currentOperation + ' ' + b + ' ';
    }
}

function dot() {
    if (needClear === true) {
        document.getElementById('text').value = document.getElementById('text').value + "\n\n";
        currentOperation = '';
        needClear = false;
    }
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    if (dotAvailable === true) {
        document.getElementById('text').value = document.getElementById('text').value + '.';
        dotAvailable = false;
        currentOperation = currentOperation + '.';
    } 
}

function clearAll() {
    document.getElementById('text').value = '';
    canWrite = true;
    operationAvailable = false;
    dotAvailable = true;
    bracketsToClose = 0;
    needClear = false;
    previousResult = 0;
    calcHistory = '';
    currentOperation = '';
}

function del() {
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    var text = document.getElementById('text').value;
    var char = text.charAt(text.length - 1);
    checkChar(char);
    if (char === " ") {
        document.getElementById('text').value = text.substr(0, text.length - 1);
        currentOperation = currentOperation.substr(0, currentOperation.length-1);
        delAfterSpace();
    } else {
        document.getElementById('text').value = text.substr(0, text.length - 1);
        currentOperation = currentOperation.substr(0, currentOperation.length-1);
    }
}

function delAfterSpace() {
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    var text = document.getElementById('text').value;
    var char = text.charAt(text.length - 1);
    checkChar(char);
    if (char === " ") {
        document.getElementById('text').value = text.substr(0, text.length - 1);
        currentOperation = currentOperation.substr(0, currentOperation.length-1);
        delAfterSpace();
    } else {
        document.getElementById('text').value = text.substr(0, text.length - 1);
        currentOperation = currentOperation.substr(0, currentOperation.length-1);
        delOnlyIfSpace();
    }
}

function delOnlyIfSpace() {
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    var text = document.getElementById('text').value;
    var char = text.charAt(text.length - 1);
    checkChar(char);
    if (char === " ") {
        document.getElementById('text').value = text.substr(0, text.length - 1);
        currentOperation = currentOperation.substr(0, currentOperation.length-1);
        delOnlyIfSpace();
    }
}

function checkChar(c) {
    if (c === ".") {
        dotAvailable = true;
    } else if (c === "(") {
        bracketsToClose = bracketsToClose - 1;
    } else if (c === ")") {
        bracketsToClose = bracketsToClose + 1;
    } else if ("*/".includes(c)) {
        operationAvailable = true;
    }
}

function clearOperation() {
    document.getElementById('text').value = calcHistory + "\n\n";
    currentOperation = '';
    dotAvailable = true
    operationAvailable = false
    bracketsToClose = 0
    needClear = false;
    previousResult = 0;
    
}