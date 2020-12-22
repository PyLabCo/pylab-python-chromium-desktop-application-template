(function() {
  update_status('시작 버튼을 눌러주세요.');

  document.querySelector('#keyword').addEventListener('keypress', function (event) {
    const code = (event.keyCode ? event.keyCode : event.which);
    if (code === 13) {
      const button = document.getElementById('action-button');
      button.focus();
      button.click();
    }
  });

  document.querySelector('#action-button').onclick = function () {
    if (document.querySelector('#action-button').textContent === '시작') {
      const headless = document.getElementById('headless').checked;
      const keyword = document.getElementById('keyword').value;

      document.getElementById('headless').disabled = true;
      document.getElementById('keyword').disabled = true;
      document.getElementById('action-button').disabled = true;

      eel.start_thread(keyword, headless)();
    } else {
      eel.terminate_thread()(function () {
        document.getElementById('headless').disabled = false;
        document.getElementById('keyword').disabled = false;
        document.getElementById('action-button').disabled = false;
        setTimeout(() => update_progress(0), 2000);
      });
    }
  };

  document.getElementById('popup-modal').addEventListener('hide.bs.modal', function () {
    document.getElementById('headless').disabled = false;
    document.getElementById('keyword').disabled = false;
    document.getElementById('action-button').disabled = false;
    update_progress(0);
  });
}());
