/* Progressive enhancement: the complete article list remains available without JS. */
(function () {
  'use strict';
  var controls = document.getElementById('article-controls');
  var list = document.getElementById('article-list');
  if (!controls || !list) return;
  var input = document.getElementById('article-query');
  var reset = document.getElementById('article-reset');
  var status = document.getElementById('article-status');
  var empty = document.getElementById('article-empty');
  var bar = document.getElementById('filter-bar');
  var english = document.documentElement.lang === 'en';
  var activeTheme = '';
  var timer;
  var labels = {beginner: 'パーク初心者ガイド', trivia: 'パークの豆知識', character: 'キャラクター図鑑',
    movie: '映画・作品の雑学', parade: 'パレード・ショー', tips: 'パークを楽しむヒント'};
  function normalize(text) {
    return text.normalize('NFKC').toLocaleLowerCase(english ? 'en' : 'ja').replace(/[\u30a1-\u30f6]/g, function (c) {
      return String.fromCharCode(c.charCodeAt(0) - 0x60);
    });
  }
  var items = Array.prototype.map.call(list.children, function (element) {
    var tag = element.querySelector('.tag');
    var card = element.querySelector('[data-theme]');
    var heading = element.querySelector('h2, h3');
    var summary = element.querySelector('p');
    return {
      element: element,
      theme: card ? card.dataset.theme : (tag ? tag.textContent.trim() : ''),
      search: normalize((heading ? heading.textContent : '') + ' ' + (summary ? summary.textContent : ''))
    };
  });
  function update() {
    clearTimeout(timer);
    var words = normalize(input.value).trim().split(/\s+/).filter(Boolean);
    var count = 0;
    items.forEach(function (item) {
      var visible = (!activeTheme || item.theme === activeTheme) && words.every(function (word) {
        return item.search.indexOf(word) !== -1;
      });
      item.element.hidden = !visible;
      if (visible) count += 1;
    });
    status.textContent = english ? count + ' of ' + items.length + ' articles' : items.length + '件中' + count + '件を表示';
    empty.hidden = count !== 0;
    reset.disabled = !input.value && !activeTheme;
  }
  if (bar) {
    var counts = new Map();
    items.forEach(function (item) { counts.set(item.theme, (counts.get(item.theme) || 0) + 1); });
    function chip(label, key, count) {
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'filter-chip';
      button.dataset.key = key;
      button.setAttribute('aria-pressed', key ? 'false' : 'true');
      button.setAttribute('aria-controls', 'article-list');
      button.textContent = label + '（' + count + '）';
      bar.appendChild(button);
    }
    chip('すべて', '', items.length);
    // Use the card's existing theme, not a second per-article category map.
    counts.forEach(function (count, theme) { if (theme) chip(labels[theme] || theme, theme, count); });
    bar.addEventListener('click', function (event) {
      var button = event.target.closest('.filter-chip');
      if (!button) return;
      activeTheme = button.dataset.key;
      Array.prototype.forEach.call(bar.children, function (other) {
        other.setAttribute('aria-pressed', other === button ? 'true' : 'false');
      });
      update();
    });
  }
  input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(update, 150); });
  reset.addEventListener('click', function () {
    input.value = '';
    activeTheme = '';
    if (bar) Array.prototype.forEach.call(bar.children, function (button) {
      button.setAttribute('aria-pressed', button.dataset.key ? 'false' : 'true');
    });
    update();
    input.focus();
  });
  controls.hidden = false;
  update();
})();
