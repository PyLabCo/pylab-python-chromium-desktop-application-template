eel.expose(update_progress);
eel.expose(update_status);
eel.expose(update_license);
eel.expose(show_popup);
eel.expose(change_elem_text);
eel.expose(change_elem_value);
eel.expose(change_elem_able);
eel.expose(add_elem_class);
eel.expose(remove_elem_class);
eel.expose(play_success_sound);

moment.locale('ko');

let timer = null;

(function() {
  update_license();

  // 타이틀
  eel.get_title()(function (title) {
    document.title = title;
  });

  // 타이틀 버전
  eel.get_title_version()(function (titleVersion) {
    document.getElementById('title-version').textContent = titleVersion;
  });

  // 툴팁 활성화
  let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  // 홈페이지 연결
  document.getElementById('pylab-logo').addEventListener('click', function() {
    eel.open_pylab()();
  });
}());

function update_progress(progress) {
  if (progress === 0) {
    document.querySelector('.progress').classList.add('hidden');
  } else {
    document.querySelector('.progress').classList.remove('hidden');
  }
  const bar = document.querySelector('.progress-bar');
  bar.setAttribute('aria-valuenow', progress);
  bar.style.width = `${progress}%`;
}

function update_status(status) {
  document.querySelector('.status').textContent = status;
}

function update_license() {
  eel.is_authenticated()(function (authenticated) {
    const license = document.querySelector('.license');
    if (authenticated) {
      license.textContent = '라이센스 상태 (활성)';
    } else {
      license.textContent = '라이센스 상태 (만료)';
    }
  });
}

function show_popup(code, message, timeout) {
  if (code) {
    document.querySelector('#popup-modal .modal-title').innerHTML = '<h3><span class="badge badge-success">성공</span></h3>';
  } else {
    document.querySelector('#popup-modal .modal-title').innerHTML = '<h3><span class="badge badge-warning">실패</span></h3>';
  }
  document.querySelector('#popup-modal .modal-body').textContent = message;
  const modal = new bootstrap.Modal(document.getElementById('popup-modal'));
  modal.show();

  if (timeout) {
    setTimeout(() => modal.hide(), timeout);
  }
}

function play_success_sound() {
  document.getElementById("success-sound").play();
}

function play_failure_sound() {
  document.getElementById("failure-sound").play();
}

function change_button_name(elem_id, name) {
  document.getElementById(elem_id).textContent = name;
}

function change_button_able(elem_id, able) {
  document.getElementById(elem_id).disabled = !able;
}

function change_elem_text(elem_id, text) {
  document.getElementById(elem_id).textContent = text;
}

function change_elem_value(elem_id, value) {
  document.getElementById(elem_id).value = value;
}

function change_elem_able(elem_id, able) {
  document.getElementById(elem_id).disabled = !able;
}

function add_elem_class(elem_id, _class) {
  document.getElementById(elem_id).classList.add(_class);
}

function remove_elem_class(elem_id, _class) {
  document.getElementById(elem_id).classList.remove(_class);
}

const array_to_table = function (data, options) {
  "use strict";

  let table = document.createElement('table'),
    thead,
    tbody,
    tfoot,
    rows = [],
    row,
    i,
    j,
    defaults = {
      th: true, // should we use th elemenst for the first row
      thead: false, //should we incldue a thead element with the first row
      tfoot: false, // should we include a tfoot element with the last row
      attrs: {} // attributes for the table element, can be used to
    };

  options = { ...defaults, ...options };

  table.classList.add('table');
  table.classList.add('table-striped');
  table.classList.add('table-hover');

  // loop through all the rows, we will deal with tfoot and thead later
  for (i = 0; i < data.length; i = i + 1) {
    row = document.createElement('tr');
    for (j = 0; j < data[i].length; j = j + 1) {
      if (i === 0 && options.th) {
        let th = document.createElement('th');
        th.innerHTML = data[i][j];
        row.appendChild(th);
      } else {
        let td = document.createElement('td');
        td.innerHTML = data[i][j];
        row.appendChild(td);
      }
    }
    rows.push(row);
  }

  // if we want a thead use shift to get it
  if (options.thead) {
    thead = rows.shift();
    let temp = document.createElement('thead');
    temp.appendChild(thead);
    thead = temp;
    thead.classList.add('thead-dark');
    table.append(thead);
  }

  // if we want a tfoot then pop it off for later use
  if (options.tfoot) {
    tfoot = rows.pop();
  }

  // add all the rows
  tbody = document.createElement('tbody');
  for (i = 0; i < rows.length; i = i + 1) {
    tbody.appendChild(rows[i]);
  }
  table.appendChild(tbody);

  // and finally add the footer if needed
  if (options.tfoot) {
    let temp = document.createElement('tfoot')
    temp.appendChild(tfoot);
    tfoot = temp;
    table.append(tfoot);
  }

  return table;
};

