(function () {
  function setButtonState(btn, liked, count) {
    btn.setAttribute('data-is-liked', liked ? 'true' : 'false');
    btn.classList.toggle('btn-warning', liked);
    btn.classList.toggle('btn-default', !liked);
    var countNode = btn.querySelector('.like-count');
    if (countNode && typeof count !== 'undefined') countNode.textContent = count;
  }

  document.addEventListener('click', function (event) {
    var btn = event.target.closest ? event.target.closest('.like-btn') : null;
    if (!btn || btn.disabled) return;
    var userId = btn.getAttribute('data-current-user-id');
    if (!userId) {
      alert('请先登录后再点赞');
      return;
    }
    fetch('/article/like/ajax', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({article_id: btn.getAttribute('data-article-id')})
    }).then(function (res) { return res.json(); })
      .then(function (data) {
        if (!data.success) { alert(data.message || '操作失败'); return; }
        setButtonState(btn, data.liked, data.count);
      }).catch(function () { alert('网络错误，请稍后再试'); });
  });
})();
