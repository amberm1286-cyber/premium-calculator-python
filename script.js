const display = document.getElementById("display");
const historyPanel = document.getElementById("historyPanel");
const angleBtn = document.getElementById("angleBtn");

let memory = 0;
let degMode = true;
let historyVisible = false;
let pendingPowerBase = null;

/* BASIC */
function append(val) {
  display.value += val;
}

function appendPi() {
  display.value += "π";
}

function clearDisplay() {
  display.value = "";
  pendingPowerBase = null;
}

function backspace() {
  display.value = display.value.slice(0, -1);
}

function toggleAngle() {
  degMode = !degMode;
  angleBtn.textContent = degMode ? "DEG" : "RAD";
}

/* HISTORY */
function addHistory(expression, result) {
  const div = document.createElement("div");
  div.className = "history-item";
  div.textContent = `${expression} = ${result}`;
  historyPanel.prepend(div);
}

function toggleHistory() {
  historyVisible = !historyVisible;
  historyPanel.style.display = historyVisible ? "block" : "none";
}

function clearHistory() {
  historyPanel.innerHTML = "";
}

function saveHistory() {
  const text = historyPanel.innerText || "";
  const blob = new Blob([text], { type: "text/plain" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "history.txt";
  link.click();
}

/* MEMORY */
function memoryAdd() {
  memory += parseFloat(display.value) || 0;
}

function memorySubtract() {
  memory -= parseFloat(display.value) || 0;
}

function memoryRecall() {
  display.value = String(memory);
}

function memoryClear() {
  memory = 0;
}

/* SAFE EVALUATION */
function preprocessExpression(expression) {
  return expression
    .replace(/÷/g, "/")
    .replace(/×/g, "*")
    .replace(/−/g, "-")
    .replace(/π/g, `(${Math.PI})`);
}

function isSafeExpression(expression) {
  return /^[0-9+\-*/().%\s]*$/.test(expression);
}

function calculate() {
  try {
    let expression = preprocessExpression(display.value);

    if (pendingPowerBase !== null) {
      const exponent = parseFloat(expression);
      if (Number.isNaN(exponent)) throw new Error("Invalid exponent");
      const result = Math.pow(pendingPowerBase, exponent);
      addHistory(`${pendingPowerBase} ^ ${exponent}`, result);
      display.value = result;
      pendingPowerBase = null;
      return;
    }

    if (!isSafeExpression(expression)) {
      throw new Error("Unsafe expression");
    }

    const result = Function(`"use strict"; return (${expression})`)();
    addHistory(display.value, result);
    display.value = result;
  } catch {
    display.value = "Error";
    pendingPowerBase = null;
  }
}

function safeCurrentNumber() {
  return parseFloat(preprocessExpression(display.value));
}

/* SCIENTIFIC */
function sinFunc() {
  let v = safeCurrentNumber();
  if (isNaN(v)) return;
  const input = v;
  if (degMode) v = v * Math.PI / 180;
  const result = Math.sin(v);
  addHistory(`sin(${input}${degMode ? "°" : ""})`, result);
  display.value = result;
}

function cosFunc() {
  let v = safeCurrentNumber();
  if (isNaN(v)) return;
  const input = v;
  if (degMode) v = v * Math.PI / 180;
  const result = Math.cos(v);
  addHistory(`cos(${input}${degMode ? "°" : ""})`, result);
  display.value = result;
}

function tanFunc() {
  let v = safeCurrentNumber();
  if (isNaN(v)) return;
  const input = v;
  if (degMode) v = v * Math.PI / 180;
  const result = Math.tan(v);
  addHistory(`tan(${input}${degMode ? "°" : ""})`, result);
  display.value = result;
}

function logFunc() {
  const v = safeCurrentNumber();
  if (isNaN(v) || v <= 0) {
    display.value = "Error";
    return;
  }
  const result = Math.log10(v);
  addHistory(`log(${v})`, result);
  display.value = result;
}

function lnFunc() {
  const v = safeCurrentNumber();
  if (isNaN(v) || v <= 0) {
    display.value = "Error";
    return;
  }
  const result = Math.log(v);
  addHistory(`ln(${v})`, result);
  display.value = result;
}

function sqrtFunc() {
  const v = safeCurrentNumber();
  if (isNaN(v) || v < 0) {
    display.value = "Error";
    return;
  }
  const result = Math.sqrt(v);
  addHistory(`√(${v})`, result);
  display.value = result;
}

function square() {
  const v = safeCurrentNumber();
  if (isNaN(v)) return;
  const result = Math.pow(v, 2);
  addHistory(`${v}²`, result);
  display.value = result;
}

function cube() {
  const v = safeCurrentNumber();
  if (isNaN(v)) return;
  const result = Math.pow(v, 3);
  addHistory(`${v}³`, result);
  display.value = result;
}

function cuberoot() {
  const v = safeCurrentNumber();
  if (isNaN(v)) return;
  const result = Math.cbrt(v);
  addHistory(`∛(${v})`, result);
  display.value = result;
}

function powerMode() {
  const base = safeCurrentNumber();
  if (isNaN(base)) return;
  pendingPowerBase = base;
  addHistory("Power mode", `Base = ${base}, enter exponent and press =`);
  display.value = "";
}

function factorialClick() {
  const n = parseInt(display.value, 10);
  if (isNaN(n) || n < 0 || String(n) !== String(parseFloat(display.value))) {
    display.value = "Error";
    return;
  }
  let res = 1;
  for (let i = 1; i <= n; i++) res *= i;
  addHistory(`${n}!`, res);
  display.value = res;
}

function percent() {
  const v = safeCurrentNumber();
  if (isNaN(v)) return;
  const result = v / 100;
  addHistory(`${v}%`, result);
  display.value = result;
}

function reciprocal() {
  const v = safeCurrentNumber();
  if (isNaN(v) || v === 0) {
    display.value = "Error";
    return;
  }
  const result = 1 / v;
  addHistory(`1/(${v})`, result);
  display.value = result;
}

function toggleSign() {
  const v = safeCurrentNumber();
  if (isNaN(v)) return;
  display.value = -v;
}

function expFunc() {
  const v = safeCurrentNumber();
  if (isNaN(v)) return;
  const result = Math.exp(v);
  addHistory(`exp(${v})`, result);
  display.value = result;
}

/* THEME */
function toggleTheme() {
  document.body.classList.toggle("light-mode");
}

/* VOICE */
function startVoice() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {
    alert("Voice input is not supported in this browser.");
    return;
  }

  const rec = new SR();
  rec.start();

  rec.onresult = (e) => {
    let t = e.results[0][0].transcript.toLowerCase();

    t = t
      .replace(/plus/g, "+")
      .replace(/minus/g, "-")
      .replace(/into/g, "*")
      .replace(/multiply/g, "*")
      .replace(/times/g, "*")
      .replace(/divide/g, "/")
      .replace(/divided by/g, "/")
      .replace(/pi/g, "π");

    display.value = t;
  };
}

/* KEYBOARD SUPPORT */
/* Python-style shortcuts:
   0–9, + - * /, ., (, ), Enter, Backspace, Esc,
   S sin, C cos, T tan, L log, N ln, R sqrt, P pi, % percent, ! factorial
*/
document.addEventListener("keydown", (e) => {
  const key = e.key;
  const lower = key.toLowerCase();

  if (!isNaN(key)) {
    e.preventDefault();
    append(key);
    return;
  }

  if (["+", "-", "*", "/", ".", "(", ")"].includes(key)) {
    e.preventDefault();
    append(key);
    return;
  }

  if (key === "Enter") {
    e.preventDefault();
    calculate();
    return;
  }

  if (key === "Backspace") {
    e.preventDefault();
    backspace();
    return;
  }

  if (key === "Escape") {
    e.preventDefault();
    clearDisplay();
    return;
  }

  if (key === "%") {
    e.preventDefault();
    percent();
    return;
  }

  if (key === "!") {
    e.preventDefault();
    factorialClick();
    return;
  }

  if (lower === "s") {
    e.preventDefault();
    sinFunc();
    return;
  }

  if (lower === "c") {
    e.preventDefault();
    cosFunc();
    return;
  }

  if (lower === "t") {
    e.preventDefault();
    tanFunc();
    return;
  }

  if (lower === "l") {
    e.preventDefault();
    logFunc();
    return;
  }

  if (lower === "n") {
    e.preventDefault();
    lnFunc();
    return;
  }

  if (lower === "r") {
    e.preventDefault();
    sqrtFunc();
    return;
  }

  if (lower === "p") {
    e.preventDefault();
    appendPi();
  }
});