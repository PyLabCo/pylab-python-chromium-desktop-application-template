# coding: utf-8
import os
import json
import logging
import sys
import traceback
import webbrowser
import zlib
from pathlib import Path
from tkinter import Tk, filedialog, messagebox, PhotoImage
from logging.handlers import TimedRotatingFileHandler
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from typing import List

import chromedriver_autoinstaller
import gevent
import eel
from pylab import keg

__author__ = "PyLab"
__license__ = "MIT"

__title__ = "PyLab 템플릿"
__version__ = "1.0.0"
__maintainer__ = "PyLab"
__email__ = "yeongbin.jo@pylab.co"
__status__ = "Production"


# noinspection PyArgumentList
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(message)s]',
    handlers=[TimedRotatingFileHandler(filename='run.log', when='midnight', interval=1, encoding='utf-8')]
)

# bootstrap or react
TARGET = 'bootstrap'

# Keg API Key
KEG_API_KEY = 'bc963eac-09b0-4911-91b0-273ea2101e5a'

# 기본 설정 값
DEFAULT_CONFIG = {}

# 단일 백그라운드 작업용 greenlet thread 객체
glt = None


def log(message):
    """로그 함수"""
    eel.update_status(message)
    logging.info(message)


@eel.expose
def terminate_thread():
    """
    스레드를 종료

    :return:
    """
    global glt
    gevent.kill(glt)
    log('사용자 입력에 의해 작업을 중단합니다. 재시작하시려면 다시 버튼을 눌러주세요.')
    keg.log('사용자 입력에 의해 작업을 중단합니다. 재시작하시려면 다시 버튼을 눌러주세요.')
    eel.change_elem_text('action-button', '시작')
    eel.change_elem_able('action-button', True)
    eel.update_progress(100)


def _thread(*args):
    eel.change_elem_text('action-button', '중지')
    eel.change_elem_able('action-button', True)

    log('작업을 시작합니다.')
    eel.update_progress(1)

    # TODO: Implement business logic
    pass

    log('작업이 완료되었습니다.')

    eel.update_progress(100)
    eel.play_success_sound()
    eel.show_popup(True, '작업이 완료되었습니다.')

    eel.change_elem_able('action-button', False)
    eel.change_elem_text('action-button', '시작')
    eel.change_elem_able('action-button', True)


@eel.expose
def start_thread(*args):
    global glt
    glt = gevent.spawn(_thread, *args)


@eel.expose
def get_keg_api_key():
    """Keg API Key를 반환합니다"""
    return KEG_API_KEY


@eel.expose
def get_version():
    """현재 버전을 반환합니다"""
    return __version__


@eel.expose
def get_title():
    """프로그램 이름을 반환합니다"""
    return __title__


@eel.expose
def get_title_version():
    """프로그램 이름과 버전을 반환합니다"""
    return f'{__title__} v{__version__}'


@eel.expose
def get_chrome_version():
    """PC에 설치된 크롬 버전을 반환합니다"""
    return chromedriver_autoinstaller.get_chrome_version()


@eel.expose
def is_authenticated():
    return keg.is_authenticated()


def setup_background_tk() -> Tk:
    """tkinter 다이얼로그만을 노출하기 위한 셋업"""
    root = Tk()
    root.withdraw()
    root.update()
    root.wm_attributes('-topmost', 1)
    root.tk.call('wm', 'iconphoto', root._w,
                 PhotoImage(file=str(Path(f'./{TARGET}/favicon.png'))))
    root.update()
    return root


def teardown_background_tk(root: Tk):
    """tkinter 다이얼로그 노출 후 정리"""
    root.update()
    root.wm_attributes('-topmost', 0)
    root.update()
    root.destroy()
    return root


@eel.expose
def open_filepath_dialog(filetypes: list):
    """Eel을 사용하지 않는 tkinter 기반 파일 선택 다이얼로그"""
    root = setup_background_tk()
    initial_dir = os.getcwd()
    filepath = filedialog.askopenfilename(
        initialdir=initial_dir,
        filetypes=filetypes
    )
    teardown_background_tk(root)
    return filepath


@eel.expose
def open_warning_dialog(message: str):
    """Eel을 사용하지 않는 tkinter 기반 경고창 출력"""
    root = setup_background_tk()
    messagebox.showwarning(title='알림', message=message)
    teardown_background_tk(root)


def obscure(payload: str) -> str:
    """문자열 난독화"""
    return b64e(zlib.compress(payload.encode('utf-8'), 9)).decode('utf-8')


def unobscure(payload: str) -> str:
    """난독화 된 문자열 복원"""
    return zlib.decompress(b64d(payload.encode('utf-8'))).decode('utf-8')


@eel.expose
def open_pylab():
    webbrowser.open('https://pylab.co')


@eel.expose
def load_config() -> dict:
    """설정 파일 로드"""
    config_file_path = Path('.') / 'config.json'
    if config_file_path.exists():
        # 설정 파일이 존재하면, 그대로 로드하여 dict 객체로 반환
        with config_file_path.open('r+') as f:
            try:
                return json.loads(f.read())
            except ValueError:
                # 설정 파일을 정상 로드할 수 없다면 기본값으로 초기화
                f.write(json.dumps(DEFAULT_CONFIG))
                return DEFAULT_CONFIG
    else:
        # 설정 파일이 존재하지 않으면, 기본값으로 생성
        with config_file_path.open('w') as f:
            f.write(json.dumps(DEFAULT_CONFIG))
            return DEFAULT_CONFIG


def save_config(c: dict):
    """설정 파일 저장"""
    config_file_path = Path('.') / 'config.json'
    with config_file_path.open('w') as f:
        f.write(json.dumps(c))


def on_close(_: str, websockets: List):
    """프로그램 종료시 호출되는 함수"""
    # 모든 페이지가 종료되었을 때만 프로세스 종료
    if len(websockets) > 0:
        return

    # 프로세스를 종료하기 전에 현재의 설정을 설정파일에 기록한다
    global config
    try:
        save_config(config)
    except:
        pass

    # 프로세스 종료
    sys.exit(0)


if __name__ == '__main__':
    # 설정 로드
    config = load_config()

    # 크롬 브라우저가 설치되어 있는지 확인
    if not get_chrome_version():
        open_warning_dialog('이 프로그램을 사용하기 위해서는 크롬 브라우저가 설치되어 있어야 합니다.')
        sys.exit(0)

    # 라이센스 확인
    try:
        keg.auth(KEG_API_KEY)
    except RuntimeError:
        open_warning_dialog('라이센스가 취소되었거나 만료되었습니다.')
        sys.exit(0)

    try:
        chromedriver_autoinstaller.install(cwd=True)
        keg.log('Init')
        eel.init(TARGET)
        eel.start(
            'main.html',
            size=(800, 400),
            mode='chrome',
            port=53878,
            close_callback=on_close
        )
    except SystemExit:
        keg.log('SystemExit')
        logging.info('SystemExit')
    except:
        logging.info(traceback.format_exc())
    sys.exit(0)
