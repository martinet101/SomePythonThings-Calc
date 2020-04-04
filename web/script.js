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

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
    mode();
})

Mousetrap.bind('0', function () {
    number(0);
});

Mousetrap.bind('1', function () {
    number(1);
});

Mousetrap.bind('2', function () {
    number(2);
});

Mousetrap.bind('3', function () {
    number(3);
});

Mousetrap.bind('4', function () {
    number(4);
});

Mousetrap.bind('5', function () {
    number(5);
});

Mousetrap.bind('6', function () {
    number(6);
});

Mousetrap.bind('7', function () {
    number(7);
});

Mousetrap.bind('8', function () {
    number(8);
});

Mousetrap.bind('9', function () {
    number(9);
});

Mousetrap.bind('+', function () {
    operation("+");
});

Mousetrap.bind('-', function () {
    operation("-");
});

Mousetrap.bind('*', function () {
    operation("*");
});

Mousetrap.bind('/', function () {
    operation("/");
});

Mousetrap.bind('^', function () {
    operation("**(");
});

Mousetrap.bind('(', function () {
    bracket("(");
});

Mousetrap.bind(')', function () {
    bracket(")");
});

Mousetrap.bind('.', function () {
    dot();
});

Mousetrap.bind(',', function () {
    dot();
});

Mousetrap.bind('=', function () {
    eval_js();
});

Mousetrap.bind('enter', function () {
    eval_js();
});

Mousetrap.bind('backspace', function () {
    del();
});


var operationAvailable = false;
var dotAvailable = true;
var bracketsToClose = 0;
var needClear = false;
var previousResult = 0;
var calcHistory = '';

async function eval_js() {
    var startValue = document.getElementById('text').value;
    var s = document.getElementById('text').value;
    s = s.split('\n = ');
    s = s[s.length - 1].replace("\n", "").replace(previousResult, '');
    let result = await eel.py_eval(s)();
    document.getElementById('text').value = startValue + "\n = " + result;
    needClear = true;
    previousResult = result;
    console.log(calcHistory);
    calcHistory = document.getElementById('text').value;
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
}

function number(n) {
    if (needClear === true) {
        document.getElementById('text').value = document.getElementById('text').value + "\n\n"
        needClear = false;
    }
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    document.getElementById('text').value = document.getElementById('text').value + n;
    operationAvailable = true;
}

function operation(o) {
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    if (needClear === true) {
        document.getElementById('text').value = document.getElementById('text').value + "\n\n" + previousResult;
        needClear = false;
    }
    if ("**(/".includes(o)) {
        if (operationAvailable === true) {
            document.getElementById('text').value = document.getElementById('text').value + ' ' + o + ' ';
        }
    } else {
        document.getElementById('text').value = document.getElementById('text').value + ' ' + o + ' ';
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
            bracketsToClose = bracketsToClose - 1;
        }
    } else {
        bracketsToClose = bracketsToClose + 1;
        document.getElementById('text').value = document.getElementById('text').value + ' ' + b + ' ';
    }
}

function dot() {
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    if (dotAvailable === true) {
        document.getElementById('text').value = document.getElementById('text').value + '.';
        dotAvailable = false;
    }
}

function clearAll() {
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    document.getElementById('text').value = "";
}

function del() {
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    var text = document.getElementById('text').value;
    var char = text.charAt(text.length - 1);
    checkChar(char);
    if (char === " ") {
        document.getElementById('text').value = text.substr(0, text.length - 1);
        delAfterSpace();
    } else {
        document.getElementById('text').value = text.substr(0, text.length - 1);
    }
}

function delAfterSpace() {
    document.getElementById("text").scrollTop = document.getElementById("text").scrollHeight;
    var text = document.getElementById('text').value;
    var char = text.charAt(text.length - 1);
    checkChar(char);
    if (char === " ") {
        document.getElementById('text').value = text.substr(0, text.length - 1);
        delAfterSpace();
    } else {
        document.getElementById('text').value = text.substr(0, text.length - 1);
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
}
