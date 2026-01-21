(venv) PS C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM> python run_all_services.py
Starting identity on port 8085 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\identity) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[identity-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\identity']
[identity-err] INFO:     Uvicorn running on http://127.0.0.1:8085 (Press CTRL+C to quit)
[identity-err] INFO:     Started reloader process [14132] using StatReload
[identity-err] INFO:     Started server process [21424]
[identity-err] INFO:     Waiting for application startup.
[identity-err] INFO:     Application startup complete.
identity is up on port 8085
Starting transport on port 8081 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\transport) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[transport-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\transport']
[transport-err] INFO:     Uvicorn running on http://127.0.0.1:8081 (Press CTRL+C to quit)
[transport-err] INFO:     Started reloader process [19212] using StatReload
[transport-err] INFO:     Started server process [20540]
[transport-err] INFO:     Waiting for application startup.
[transport-err] INFO:     Application startup complete.
transport is up on port 8081
Starting ingestion on port 8000 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\ingestion) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
ingestion is up on port 8000
Starting patch on port 8082 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\patch) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[ingestion-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\ingestion']
[ingestion-err] INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
[ingestion-err] INFO:     Started reloader process [11756] using StatReload
[patch-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\patch']
[patch-err] INFO:     Uvicorn running on http://127.0.0.1:8082 (Press CTRL+C to quit)
[patch-err] INFO:     Started reloader process [4056] using StatReload
[patch-err] INFO:     Started server process [21148]
[patch-err] INFO:     Waiting for application startup.
[patch-err] INFO:     Application startup complete.
[ingestion-err] INFO:     Started server process [11612]
[ingestion-err] INFO:     Waiting for application startup.
[ingestion-err] INFO:     Application startup complete.
patch is up on port 8082
Starting penetration on port 8083 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\penetration) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[penetration-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\penetration']
[penetration-err] INFO:     Uvicorn running on http://127.0.0.1:8083 (Press CTRL+C to quit)
[penetration-err] INFO:     Started reloader process [20896] using StatReload
[penetration-err] INFO:     Started server process [14544]
[penetration-err] INFO:     Waiting for application startup.
[penetration-err] INFO:     Application startup complete.
penetration is up on port 8083
Starting psa on port 8001 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\psa) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[psa-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\psa']
[psa-err] INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
[psa-err] INFO:     Started reloader process [12224] using StatReload
[psa-err] INFO:     Started server process [21524]
[psa-err] INFO:     Waiting for application startup.
[psa-err] INFO:     Application startup complete.
psa is up on port 8001
Starting siem on port 8002 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\siem) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[siem-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\siem']
[siem-err] INFO:     Uvicorn running on http://127.0.0.1:8002 (Press CTRL+C to quit)
[siem-err] INFO:     Started reloader process [13912] using StatReload
[siem-err] C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\pydantic\_internal\_config.py:383: UserWarning: Valid config keys have changed in V2:
[siem-err] * 'orm_mode' has been renamed to 'from_attributes'
[siem-err]   warnings.warn(message, UserWarning)
[siem-err] INFO:     Started server process [21164]
[siem-err] INFO:     Waiting for application startup.
[siem-err] INFO:     Application startup complete.
siem is up on port 8002
Starting edr on port 8003 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\edr) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[edr-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\edr']
[edr-err] INFO:     Uvicorn running on http://127.0.0.1:8003 (Press CTRL+C to quit)
[edr-err] INFO:     Started reloader process [6904] using StatReload
[edr-err] INFO:     Started server process [21900]
[edr-err] INFO:     Waiting for application startup.
[edr-err] INFO:     Application startup complete.
edr is up on port 8003
Starting vulnerability on port 8004 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\vulnerability) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[vulnerability-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\vulnerability']
[vulnerability-err] INFO:     Uvicorn running on http://127.0.0.1:8004 (Press CTRL+C to quit)
[vulnerability-err] INFO:     Started reloader process [14452] using StatReload
[vulnerability-err] INFO:     Started server process [5384]
[vulnerability-err] INFO:     Waiting for application startup.
[vulnerability-err] INFO:     Application startup complete.
vulnerability is up on port 8004
Starting auditing on port 8010 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\auditing) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[auditing-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\auditing']
[auditing-err] INFO:     Uvicorn running on http://127.0.0.1:8010 (Press CTRL+C to quit)
[auditing-err] INFO:     Started reloader process [12736] using StatReload
[auditing-err] INFO:     Started server process [9652]
[auditing-err] INFO:     Waiting for application startup.
[auditing-err] INFO:     Application startup complete.
auditing is up on port 8010
Starting rmm on port 8020 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\rmm) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[rmm-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\rmm']
[rmm-err] INFO:     Uvicorn running on http://127.0.0.1:8020 (Press CTRL+C to quit)
[rmm-err] INFO:     Started reloader process [19264] using StatReload
[rmm-err] INFO:     Started server process [11976]
[rmm-err] INFO:     Waiting for application startup.
[rmm-err] INFO:     Application startup complete.
rmm is up on port 8020
Shutting down services...
[vulnerability-err] INFO:     Shutting down
[edr-err] INFO:     Shutting down
[ingestion-err] INFO:     Shutting down
[patch-err] INFO:     Shutting down
[transport-err] INFO:     Shutting down
[auditing-err] INFO:     Shutting down
[psa-err] INFO:     Shutting down
[siem-err] INFO:     Shutting down
[identity-err] INFO:     Shutting down
[rmm-err] INFO:     Shutting down
[penetration-err] INFO:     Shutting down
[edr-err] INFO:     Waiting for application shutdown.
[edr-err] INFO:     Application shutdown complete.
[edr-err] INFO:     Finished server process [21900]
[vulnerability-err] INFO:     Waiting for application shutdown.
[vulnerability-err] INFO:     Application shutdown complete.
[vulnerability-err] INFO:     Finished server process [5384]
[ingestion-err] INFO:     Waiting for application shutdown.
[ingestion-err] INFO:     Application shutdown complete.
[ingestion-err] INFO:     Finished server process [11612]
[patch-err] INFO:     Waiting for application shutdown.
[patch-err] INFO:     Application shutdown complete.
[patch-err] INFO:     Finished server process [21148]
[transport-err] INFO:     Waiting for application shutdown.
[transport-err] INFO:     Application shutdown complete.
[transport-err] INFO:     Finished server process [20540]
[auditing-err] INFO:     Waiting for application shutdown.
[auditing-err] INFO:     Application shutdown complete.
[auditing-err] INFO:     Finished server process [9652]
[psa-err] INFO:     Waiting for application shutdown.
[psa-err] INFO:     Application shutdown complete.
[psa-err] INFO:     Finished server process [21524]
[identity-err] INFO:     Waiting for application shutdown.
[identity-err] INFO:     Application shutdown complete.
[identity-err] INFO:     Finished server process [21424]
[siem-err] INFO:     Waiting for application shutdown.
[siem-err] INFO:     Application shutdown complete.
[siem-err] INFO:     Finished server process [21164]
[rmm-err] INFO:     Waiting for application shutdown.
[rmm-err] INFO:     Application shutdown complete.
[rmm-err] INFO:     Finished server process [11976]
[penetration-err] INFO:     Waiting for application shutdown.
[penetration-err] INFO:     Application shutdown complete.
[penetration-err] INFO:     Finished server process [14544]
Exception ignored while calling deallocator <function _ProactorBasePipeTransport.__del__ at 0x00000215C29214E0>:
Traceback (most recent call last):
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 116, in __del__
    _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 80, in __repr__
    info.append(f'fd={self._sock.fileno()}')
  File "C:\Python314\Lib\asyncio\windows_utils.py", line 102, in fileno
    raise ValueError("I/O operation on closed pipe")
ValueError: I/O operation on closed pipe
Exception ignored while calling deallocator <function _ProactorBasePipeTransport.__del__ at 0x00000215C29214E0>:
Traceback (most recent call last):
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 116, in __del__
    _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 80, in __repr__
    info.append(f'fd={self._sock.fileno()}')
  File "C:\Python314\Lib\asyncio\windows_utils.py", line 102, in fileno
    raise ValueError("I/O operation on closed pipe")
ValueError: I/O operation on closed pipe
Exception ignored while calling deallocator <function _ProactorBasePipeTransport.__del__ at 0x00000215C29214E0>:
Traceback (most recent call last):
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 116, in __del__
    _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 80, in __repr__
    info.append(f'fd={self._sock.fileno()}')
  File "C:\Python314\Lib\asyncio\windows_utils.py", line 102, in fileno
    raise ValueError("I/O operation on closed pipe")
ValueError: I/O operation on closed pipe
Exception ignored while calling deallocator <function _ProactorBasePipeTransport.__del__ at 0x00000215C29214E0>:
Traceback (most recent call last):
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 116, in __del__
    _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 80, in __repr__
    info.append(f'fd={self._sock.fileno()}')
  File "C:\Python314\Lib\asyncio\windows_utils.py", line 102, in fileno
    raise ValueError("I/O operation on closed pipe")
ValueError: I/O operation on closed pipe
Exception ignored while calling deallocator <function _ProactorBasePipeTransport.__del__ at 0x00000215C29214E0>:
Traceback (most recent call last):
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 116, in __del__
    _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 80, in __repr__
    info.append(f'fd={self._sock.fileno()}')
  File "C:\Python314\Lib\asyncio\windows_utils.py", line 102, in fileno
    raise ValueError("I/O operation on closed pipe")
ValueError: I/O operation on closed pipe
Exception ignored while calling deallocator <function _ProactorBasePipeTransport.__del__ at 0x00000215C29214E0>:
Traceback (most recent call last):
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 116, in __del__
    _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 80, in __repr__
    info.append(f'fd={self._sock.fileno()}')
  File "C:\Python314\Lib\asyncio\windows_utils.py", line 102, in fileno
    raise ValueError("I/O operation on closed pipe")
ValueError: I/O operation on closed pipe
Exception ignored while calling deallocator <function _ProactorBasePipeTransport.__del__ at 0x00000215C29214E0>:
Traceback (most recent call last):
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 116, in __del__
    _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 80, in __repr__
    info.append(f'fd={self._sock.fileno()}')
  File "C:\Python314\Lib\asyncio\windows_utils.py", line 102, in fileno
    raise ValueError("I/O operation on closed pipe")
ValueError: I/O operation on closed pipe
Exception ignored while calling deallocator <function _ProactorBasePipeTransport.__del__ at 0x00000215C29214E0>:
Traceback (most recent call last):
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 116, in __del__
    _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
  File "C:\Python314\Lib\asyncio\proactor_events.py", line 80, in __repr__
    info.append(f'fd={self._sock.fileno()}')
  File "C:\Python314\Lib\asyncio\windows_utils.py", line 102, in fileno
    raise ValueError("I/O operation on closed pipe")
ValueError: I/O operation on closed pipe
(venv) PS C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM> python run_all_services.py
Starting identity on port 8085 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\identity) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[identity-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\identity']
[identity-err] INFO:     Uvicorn running on http://127.0.0.1:8085 (Press CTRL+C to quit)
[identity-err] INFO:     Started reloader process [15364] using StatReload
[identity-err] INFO:     Started server process [15468]
[identity-err] INFO:     Waiting for application startup.
[identity-err] INFO:     Application startup complete.
identity is up on port 8085
Starting transport on port 8081 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\transport) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[transport-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\transport']
[transport-err] INFO:     Uvicorn running on http://127.0.0.1:8081 (Press CTRL+C to quit)
[transport-err] INFO:     Started reloader process [20960] using StatReload
[transport-err] INFO:     Started server process [10880]
[transport-err] INFO:     Waiting for application startup.
[transport-err] INFO:     Application startup complete.
transport is up on port 8081
Starting ingestion on port 8000 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\ingestion) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
ingestion is up on port 8000
Starting patch on port 8082 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\patch) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[ingestion-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\ingestion']
[ingestion-err] INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
[ingestion-err] INFO:     Started reloader process [21972] using StatReload
[patch-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\patch']
[patch-err] INFO:     Uvicorn running on http://127.0.0.1:8082 (Press CTRL+C to quit)
[patch-err] INFO:     Started reloader process [14488] using StatReload
[patch-err] INFO:     Started server process [21080]
[patch-err] INFO:     Waiting for application startup.
[patch-err] INFO:     Application startup complete.
[ingestion-err] INFO:     Started server process [18240]
[ingestion-err] INFO:     Waiting for application startup.
patch is up on port 8082
Starting penetration on port 8083 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\penetration) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[ingestion-err] ERROR:    Traceback (most recent call last):
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\starlette\routing.py", line 694, in lifespan
[ingestion-err]     async with self.lifespan_context(app) as maybe_state:
[ingestion-err]                ~~~~~~~~~~~~~~~~~~~~~^^^^^
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\starlette\routing.py", line 571, in __aenter__
[ingestion-err]     await self._router.startup()
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\starlette\routing.py", line 671, in startup
[ingestion-err]     await handler()
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\ingestion\app\main.py", line 119, in startup
[ingestion-err]     pool = await asyncpg.create_pool(
[ingestion-err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^
[ingestion-err]     ...<3 lines>...
[ingestion-err]     )
[ingestion-err]     ^
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\asyncpg\pool.py", line 439, in _async__init__
[ingestion-err]     await self._initialize()
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\asyncpg\pool.py", line 466, in _initialize
[ingestion-err]     await first_ch.connect()
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\asyncpg\pool.py", line 153, in connect
[ingestion-err]     self._con = await self._pool._get_new_connection()
[ingestion-err]                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\asyncpg\pool.py", line 538, in _get_new_connection
[ingestion-err]     con = await self._connect(
[ingestion-err]           ^^^^^^^^^^^^^^^^^^^^
[ingestion-err]     ...<5 lines>...
[ingestion-err]     )
[ingestion-err]     ^
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\asyncpg\connection.py", line 2443, in connect
[ingestion-err]     return await connect_utils._connect(
[ingestion-err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[ingestion-err]     ...<22 lines>...
[ingestion-err]     )
[ingestion-err]     ^
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\asyncpg\connect_utils.py", line 1218, in _connect
[ingestion-err]     conn = await _connect_addr(
[ingestion-err]            ^^^^^^^^^^^^^^^^^^^^
[ingestion-err]     ...<6 lines>...
[ingestion-err]     )
[ingestion-err]     ^
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\asyncpg\connect_utils.py", line 1050, in _connect_addr      
[ingestion-err]     return await __connect_addr(params, False, *args)
[ingestion-err]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[ingestion-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\asyncpg\connect_utils.py", line 1102, in __connect_addr     
[ingestion-err]     await connected
[ingestion-err] asyncpg.exceptions.InvalidPasswordError: password authentication failed for user "tamsilsiem"
[ingestion-err]
[ingestion-err] ERROR:    Application startup failed. Exiting.
[penetration-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\penetration']
[penetration-err] INFO:     Uvicorn running on http://127.0.0.1:8083 (Press CTRL+C to quit)
[penetration-err] INFO:     Started reloader process [21008] using StatReload
[penetration-err] INFO:     Started server process [7584]
[penetration-err] INFO:     Waiting for application startup.
[penetration-err] INFO:     Application startup complete.
penetration is up on port 8083
Starting psa on port 8001 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\psa) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[psa-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\psa']
[psa-err] INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
[psa-err] INFO:     Started reloader process [7328] using StatReload
[psa-err] INFO:     Started server process [21728]
[psa-err] INFO:     Waiting for application startup.
[psa-err] INFO:     Application startup complete.
psa is up on port 8001
Starting siem on port 8002 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\siem) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[siem-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\siem']
[siem-err] INFO:     Uvicorn running on http://127.0.0.1:8002 (Press CTRL+C to quit)
[siem-err] INFO:     Started reloader process [16432] using StatReload
[siem-err] C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\pydantic\_internal\_config.py:383: UserWarning: Valid config keys have changed in V2:
[siem-err] * 'orm_mode' has been renamed to 'from_attributes'
[siem-err]   warnings.warn(message, UserWarning)
[siem-err] INFO:     Started server process [19124]
[siem-err] INFO:     Waiting for application startup.
[siem-err] INFO:     Application startup complete.
siem is up on port 8002
Starting edr on port 8003 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\edr) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[edr-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\edr']
[edr-err] INFO:     Uvicorn running on http://127.0.0.1:8003 (Press CTRL+C to quit)
[edr-err] INFO:     Started reloader process [20624] using StatReload
[psa] INFO:     10.252.0.2:54226 - "POST /upload HTTP/1.1" 404 Not Found
[edr-err] INFO:     Started server process [9116]
[edr-err] INFO:     Waiting for application startup.
[edr-err] INFO:     Application startup complete.
edr is up on port 8003
Starting vulnerability on port 8004 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\vulnerability) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[vulnerability-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\vulnerability']
[vulnerability-err] INFO:     Uvicorn running on http://127.0.0.1:8004 (Press CTRL+C to quit)
[vulnerability-err] INFO:     Started reloader process [17584] using StatReload
[vulnerability-err] INFO:     Started server process [4868]
[vulnerability-err] INFO:     Waiting for application startup.
[vulnerability-err] INFO:     Application startup complete.
vulnerability is up on port 8004
Starting auditing on port 8010 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\auditing) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[auditing-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\auditing']    
[auditing-err] INFO:     Uvicorn running on http://127.0.0.1:8010 (Press CTRL+C to quit)
[auditing-err] INFO:     Started reloader process [20092] using StatReload
[auditing-err] INFO:     Started server process [21016]
[auditing-err] INFO:     Waiting for application startup.
[auditing-err] INFO:     Application startup complete.
auditing is up on port 8010
Starting rmm on port 8020 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\rmm) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[rmm-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\rmm']
[rmm-err] INFO:     Uvicorn running on http://127.0.0.1:8020 (Press CTRL+C to quit)
[rmm-err] INFO:     Started reloader process [20016] using StatReload
[rmm-err] INFO:     Started server process [12260]
[rmm-err] INFO:     Waiting for application startup.
[rmm-err] INFO:     Application startup complete.
rmm is up on port 8020
