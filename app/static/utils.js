/* 
 * JavaScript Utilities
 */


function _id(id) { return document.getElementById(id); }
function _class(className) { return document.getElementsByClassName(className); }
function append(parent, el) { parent.append(el); }
function after(target, el) { target.after(el); }
function before(target, el) { target.before(el); }
function empty(el) { el.replaceChildren(); }

function addClass(el, className) { el.classList.add(className); }
function remClass(el, className) { el.classList.remove(className); } 
function hasClass(el, className) { return el.classList.includes(className); }
function replClass(el, oldClassName, newClassName) { el.classList.replace(oldClassName, newClassName); }
function toglClass(el, className) { el.classList.toggle(className); }

function hide(el) { el.style.display = 'none'; }
function show(el) { el.style.display = ''; }
function toggle(el) {
  if (el.style.display == 'none') {
    el.style.display = '';
  } else {
    el.style.display = 'none';
  }
};

async function getJSON(url) {
  constresponse = await fetch(url);
  const data = await response.json();
  return data;
};

async function postJSON(url, data) {
  await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
};

function html(el, data) { el.innerHTML = data; }
function generateElements(html) {
  const template = document.createElement('template');
  template.innerHTML = html.trim();
  return template.content.children;
};

function memoize(fn) {
  let cache = {};

  return (...args) => {
    const key = JSON.stringify(args);

    if (!cache[key]) {
      cache[key] = fn(...args);
    }

    return cache[key];
  }
};

function ready(fn) {
  if (document.readyState !== 'loading') {
    fn();
  } else {
    document.addEventListener('DOMContentLoaded', fn);
  }
};

