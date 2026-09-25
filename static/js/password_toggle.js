(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var fields = document.querySelectorAll('input[type="password"]');
    fields.forEach(function (input) {
      var group = document.createElement('div');
      group.className = 'password-wrap';
      input.parentNode.insertBefore(group, input);
      group.appendChild(input);
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'password-toggle';
      btn.textContent = '显示';
      btn.onclick = function () {
        input.type = input.type === 'password' ? 'text' : 'password';
        btn.textContent = input.type === 'password' ? '显示' : '隐藏';
      };
      group.appendChild(btn);
    });
  });
})();
