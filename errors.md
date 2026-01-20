(venv) PS C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM> python run_all_services.py
Starting identity on port 8085 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\identity) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[identity-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\identity']
[identity-err] INFO:     Uvicorn running on http://127.0.0.1:8085 (Press CTRL+C to quit)
[identity-err] INFO:     Started reloader process [15424] using StatReload
[identity-err] INFO:     Started server process [1804]
[identity-err] INFO:     Waiting for application startup.
[identity-err] INFO:     Application startup complete.
identity is up on port 8085
Starting transport on port 8081 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\transport) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[transport-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\transport']
[transport-err] INFO:     Uvicorn running on http://127.0.0.1:8081 (Press CTRL+C to quit)
[transport-err] INFO:     Started reloader process [15264] using StatReload
[transport-err] INFO:     Started server process [14212]
[transport-err] INFO:     Waiting for application startup.
[transport-err] INFO:     Application startup complete.
transport is up on port 8081
Starting ingestion on port 8000 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\ingestion) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[ingestion-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\ingestion']
[ingestion-err] INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
[ingestion-err] INFO:     Started reloader process [19196] using StatReload
[ingestion-err] INFO:     Started server process [14516]
[ingestion-err] INFO:     Waiting for application startup.
[ingestion-err] INFO:     Application startup complete.
ingestion is up on port 8000
Starting patch on port 8082 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\patch) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[patch-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\patch']
[patch-err] INFO:     Uvicorn running on http://127.0.0.1:8082 (Press CTRL+C to quit)
[patch-err] INFO:     Started reloader process [12052] using StatReload
[patch-err] Process SpawnProcess-1:
[patch-err] Traceback (most recent call last):
[patch-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 320, in _bootstrap
[patch-err]     self.run()
[patch-err]     ~~~~~~~~^^
[patch-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 108, in run
[patch-err]     self._target(*self._args, **self._kwargs)
[patch-err]     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[patch-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
[patch-err]     target(sockets=sockets)
[patch-err]     ~~~~~~^^^^^^^^^^^^^^^^^
[patch-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 67, in run
[patch-err]     return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
[patch-err]   File "C:\Python314\Lib\asyncio\runners.py", line 204, in run
[patch-err]     return runner.run(main)
[patch-err]            ~~~~~~~~~~^^^^^^
[patch-err]   File "C:\Python314\Lib\asyncio\runners.py", line 127, in run
[patch-err]     return self._loop.run_until_complete(task)
[patch-err]            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
[patch-err]   File "C:\Python314\Lib\asyncio\base_events.py", line 719, in run_until_complete
[patch-err]     return future.result()
[patch-err]            ~~~~~~~~~~~~~^^
[patch-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 71, in serve
[patch-err]     await self._serve(sockets)
[patch-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 78, in _serve
[patch-err]     config.load()
[patch-err]     ~~~~~~~~~~~^^
[patch-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\config.py", line 439, in load
[patch-err]     self.loaded_app = import_from_string(self.app)
[patch-err]                       ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
[patch-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
[patch-err]     module = importlib.import_module(module_str)
[patch-err]   File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
[patch-err]     return _bootstrap._gcd_import(name[level:], package, level)
[patch-err]            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[patch-err]   File "<frozen importlib._bootstrap>", line 1398, in _gcd_import
[patch-err]   File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
[patch-err]   File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
[patch-err]   File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
[patch-err]   File "<frozen importlib._bootstrap_external>", line 759, in exec_module
[patch-err]   File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
[patch-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\patch\app\main.py", line 415, in <module>
[patch-err]     @app.get("/plans/{plan_id}", response_model=ExecutionPlan)
[patch-err]                                                 ^^^^^^^^^^^^^
[patch-err] NameError: name 'ExecutionPlan' is not defined
WARNING: patch did not respond on port 8082 within timeout
Starting penetration on port 8083 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\penetration) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[penetration-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\penetration']
[penetration-err] INFO:     Uvicorn running on http://127.0.0.1:8083 (Press CTRL+C to quit)
[penetration-err] INFO:     Started reloader process [6176] using StatReload
[penetration-err] INFO:     Started server process [13892]
[penetration-err] INFO:     Waiting for application startup.
[penetration-err] INFO:     Application startup complete.
penetration is up on port 8083
Starting psa on port 8001 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\psa) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[psa-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\psa']
[psa-err] INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
[psa-err] INFO:     Started reloader process [17236] using StatReload
[psa-err] Process SpawnProcess-1:
[psa-err] Traceback (most recent call last):
[psa-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 320, in _bootstrap
[psa-err]     self.run()
[psa-err]     ~~~~~~~~^^
[psa-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 108, in run
[psa-err]     self._target(*self._args, **self._kwargs)
[psa-err]     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[psa-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
[psa-err]     target(sockets=sockets)
[psa-err]     ~~~~~~^^^^^^^^^^^^^^^^^
[psa-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 67, in run
[psa-err]     return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
[psa-err]   File "C:\Python314\Lib\asyncio\runners.py", line 204, in run
[psa-err]     return runner.run(main)
[psa-err]            ~~~~~~~~~~^^^^^^
[psa-err]   File "C:\Python314\Lib\asyncio\runners.py", line 127, in run
[psa-err]     return self._loop.run_until_complete(task)
[psa-err]            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
[psa-err]   File "C:\Python314\Lib\asyncio\base_events.py", line 719, in run_until_complete
[psa-err]     return future.result()
[psa-err]            ~~~~~~~~~~~~~^^
[psa-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 71, in serve
[psa-err]     await self._serve(sockets)
[psa-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 78, in _serve
[psa-err]     config.load()
[psa-err]     ~~~~~~~~~~~^^
[psa-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\config.py", line 439, in load
[psa-err]     self.loaded_app = import_from_string(self.app)
[psa-err]                       ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
[psa-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
[psa-err]     module = importlib.import_module(module_str)
[psa-err]   File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
[psa-err]     return _bootstrap._gcd_import(name[level:], package, level)
[psa-err]            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[psa-err]   File "<frozen importlib._bootstrap>", line 1398, in _gcd_import
[psa-err]   File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
[psa-err]   File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
[psa-err]   File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
[psa-err]   File "<frozen importlib._bootstrap_external>", line 755, in exec_module
[psa-err]   File "<frozen importlib._bootstrap_external>", line 893, in get_code
[psa-err]   File "<frozen importlib._bootstrap_external>", line 823, in source_to_code
[psa-err]   File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
[psa-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\psa\app\main.py", line 18
[psa-err]     from __future__ import annotations
[psa-err]     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[psa-err] SyntaxError: from __future__ imports must occur at the beginning of the file
WARNING: psa did not respond on port 8001 within timeout
Starting siem on port 8002 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\siem) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[siem-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\siem']
[siem-err] INFO:     Uvicorn running on http://127.0.0.1:8002 (Press CTRL+C to quit)
[siem-err] INFO:     Started reloader process [12792] using StatReload
[siem-err] C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\pydantic\_internal\_config.py:383: UserWarning: Valid config keys have changed in V2:
[siem-err] * 'orm_mode' has been renamed to 'from_attributes'
[siem-err]   warnings.warn(message, UserWarning)
[siem-err] Process SpawnProcess-1:
[siem-err] Traceback (most recent call last):
[siem-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 320, in _bootstrap
[siem-err]     self.run()
[siem-err]     ~~~~~~~~^^
[siem-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 108, in run
[siem-err]     self._target(*self._args, **self._kwargs)
[siem-err]     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[siem-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
[siem-err]     target(sockets=sockets)
[siem-err]     ~~~~~~^^^^^^^^^^^^^^^^^
[siem-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 67, in run
[siem-err]     return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
[siem-err]   File "C:\Python314\Lib\asyncio\runners.py", line 204, in run
[siem-err]     return runner.run(main)
[siem-err]            ~~~~~~~~~~^^^^^^
[siem-err]   File "C:\Python314\Lib\asyncio\runners.py", line 127, in run
[siem-err]     return self._loop.run_until_complete(task)
[siem-err]            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
[siem-err]   File "C:\Python314\Lib\asyncio\base_events.py", line 719, in run_until_complete
[siem-err]     return future.result()
[siem-err]            ~~~~~~~~~~~~~^^
[siem-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 71, in serve
[siem-err]     await self._serve(sockets)
[siem-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 78, in _serve
[siem-err]     config.load()
[siem-err]     ~~~~~~~~~~~^^
[siem-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\config.py", line 439, in load
[siem-err]     self.loaded_app = import_from_string(self.app)
[siem-err]                       ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
[siem-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\importer.py", line 22, in import_from_string
[siem-err]     raise exc from None
[siem-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
[siem-err]     module = importlib.import_module(module_str)
[siem-err]   File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
[siem-err]     return _bootstrap._gcd_import(name[level:], package, level)
[siem-err]            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[siem-err]   File "<frozen importlib._bootstrap>", line 1398, in _gcd_import
[siem-err]   File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
[siem-err]   File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
[siem-err]   File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
[siem-err]   File "<frozen importlib._bootstrap_external>", line 759, in exec_module
[siem-err]   File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
[siem-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\siem\app\main.py", line 2, in <module>
[siem-err]     from .api import router as siem_router
[siem-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\siem\app\api.py", line 5, in <module>
[siem-err]     from core_services.common.escalation import EscalationClient
[siem-err] ModuleNotFoundError: No module named 'core_services'
WARNING: siem did not respond on port 8002 within timeout
Starting edr on port 8003 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\edr) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[edr-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\edr']
[edr-err] INFO:     Uvicorn running on http://127.0.0.1:8003 (Press CTRL+C to quit)
[edr-err] INFO:     Started reloader process [19212] using StatReload
[edr-err] Process SpawnProcess-1:
[edr-err] Traceback (most recent call last):
[edr-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 320, in _bootstrap
[edr-err]     self.run()
[edr-err]     ~~~~~~~~^^
[edr-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 108, in run
[edr-err]     self._target(*self._args, **self._kwargs)
[edr-err]     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[edr-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
[edr-err]     target(sockets=sockets)
[edr-err]     ~~~~~~^^^^^^^^^^^^^^^^^
[edr-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 67, in run
[edr-err]     return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
[edr-err]   File "C:\Python314\Lib\asyncio\runners.py", line 204, in run
[edr-err]     return runner.run(main)
[edr-err]            ~~~~~~~~~~^^^^^^
[edr-err]   File "C:\Python314\Lib\asyncio\runners.py", line 127, in run
[edr-err]     return self._loop.run_until_complete(task)
[edr-err]            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
[edr-err]   File "C:\Python314\Lib\asyncio\base_events.py", line 719, in run_until_complete
[edr-err]     return future.result()
[edr-err]            ~~~~~~~~~~~~~^^
[edr-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 71, in serve
[edr-err]     await self._serve(sockets)
[edr-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 78, in _serve
[edr-err]     config.load()
[edr-err]     ~~~~~~~~~~~^^
[edr-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\config.py", line 439, in load
[edr-err]     self.loaded_app = import_from_string(self.app)
[edr-err]                       ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
[edr-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\importer.py", line 22, in import_from_string
[edr-err]     raise exc from None
[edr-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
[edr-err]     module = importlib.import_module(module_str)
[edr-err]   File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
[edr-err]     return _bootstrap._gcd_import(name[level:], package, level)
[edr-err]            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[edr-err]   File "<frozen importlib._bootstrap>", line 1398, in _gcd_import
[edr-err]   File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
[edr-err]   File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
[edr-err]   File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
[edr-err]   File "<frozen importlib._bootstrap_external>", line 759, in exec_module
[edr-err]   File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
[edr-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\edr\app\main.py", line 2, in <module>
[edr-err]     from .api import router as edr_router
[edr-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\edr\app\api.py", line 4, in <module>
[edr-err]     from core_services.common.escalation import EscalationClient
[edr-err] ModuleNotFoundError: No module named 'core_services'
WARNING: edr did not respond on port 8003 within timeout
Starting vulnerability on port 8004 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\vulnerability) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[vulnerability-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\vulnerability']
[vulnerability-err] INFO:     Uvicorn running on http://127.0.0.1:8004 (Press CTRL+C to quit)
[vulnerability-err] INFO:     Started reloader process [2540] using StatReload
[vulnerability-err] Process SpawnProcess-1:
[vulnerability-err] Traceback (most recent call last):
[vulnerability-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 320, in _bootstrap
[vulnerability-err]     self.run()
[vulnerability-err]     ~~~~~~~~^^
[vulnerability-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 108, in run
[vulnerability-err]     self._target(*self._args, **self._kwargs)
[vulnerability-err]     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
[vulnerability-err]     target(sockets=sockets)
[vulnerability-err]     ~~~~~~^^^^^^^^^^^^^^^^^
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 67, in run
[vulnerability-err]     return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
[vulnerability-err]   File "C:\Python314\Lib\asyncio\runners.py", line 204, in run
[vulnerability-err]     return runner.run(main)
[vulnerability-err]            ~~~~~~~~~~^^^^^^
[vulnerability-err]   File "C:\Python314\Lib\asyncio\runners.py", line 127, in run
[vulnerability-err]     return self._loop.run_until_complete(task)
[vulnerability-err]            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
[vulnerability-err]   File "C:\Python314\Lib\asyncio\base_events.py", line 719, in run_until_complete
[vulnerability-err]     return future.result()
[vulnerability-err]            ~~~~~~~~~~~~~^^
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 71, in serve
[vulnerability-err]     await self._serve(sockets)
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 78, in _serve
[vulnerability-err]     config.load()
[vulnerability-err]     ~~~~~~~~~~~^^
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\config.py", line 439, in load
[vulnerability-err]     self.loaded_app = import_from_string(self.app)
[vulnerability-err]                       ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
[vulnerability-err]     module = importlib.import_module(module_str)
[vulnerability-err]   File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
[vulnerability-err]     return _bootstrap._gcd_import(name[level:], package, level)
[vulnerability-err]            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[vulnerability-err]   File "<frozen importlib._bootstrap>", line 1398, in _gcd_import
[vulnerability-err]   File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
[vulnerability-err]   File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
[vulnerability-err]   File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
[vulnerability-err]   File "<frozen importlib._bootstrap_external>", line 759, in exec_module
[vulnerability-err]   File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\vulnerability\app\main.py", line 28, in <module>
[vulnerability-err]     from .store_sql import init_sql_store, SQLVulnerabilityStore
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\vulnerability\app\store_sql.py", line 10, in <module>
[vulnerability-err]     class VulnerabilityRecordTable(Base):
[vulnerability-err]         __tablename__ = "vulnerability_records"
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\decl_api.py", line 199, in __init__
[vulnerability-err]     _as_declarative(reg, cls, dict_)
[vulnerability-err]     ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 245, in _as_declarative
[vulnerability-err]     return _MapperConfig.setup_mapping(registry, cls, dict_, None, {})
[vulnerability-err]            ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 326, in setup_mapping
[vulnerability-err]     return _ClassScanMapperConfig(
[vulnerability-err]         registry, cls_, dict_, table, mapper_kw
[vulnerability-err]     )
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 581, in __init__
[vulnerability-err]     self._early_mapping(mapper_kw)
[vulnerability-err]     ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 367, in _early_mapping
[vulnerability-err]     self.map(mapper_kw)
[vulnerability-err]     ~~~~~~~~^^^^^^^^^^^
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 1995, in map
[vulnerability-err]     mapper_cls(self.cls, self.local_table, **self.mapper_args),
[vulnerability-err]     ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[vulnerability-err]   File "<string>", line 2, in __init__
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\util\deprecations.py", line 281, in warned
[vulnerability-err]     return fn(*args, **kwargs)  # type: ignore[no-any-return]
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 866, in __init__
[vulnerability-err]     self._configure_pks()
[vulnerability-err]     ~~~~~~~~~~~~~~~~~~~^^
[vulnerability-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\mapper.py", line 1652, in _configure_pks
[vulnerability-err]     raise sa_exc.ArgumentError(
[vulnerability-err]     ...<3 lines>...
[vulnerability-err]     )
[vulnerability-err] sqlalchemy.exc.ArgumentError: Mapper Mapper[VulnerabilityRecordTable(vulnerability_records)] could not assemble any primary key columns for mapped table 'vulnerability_records'
WARNING: vulnerability did not respond on port 8004 within timeout
Starting auditing on port 8010 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\auditing) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[auditing-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\auditing']
[auditing-err] INFO:     Uvicorn running on http://127.0.0.1:8010 (Press CTRL+C to quit)
[auditing-err] INFO:     Started reloader process [10796] using StatReload
[auditing-err] Process SpawnProcess-1:
[auditing-err] Traceback (most recent call last):
[auditing-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 320, in _bootstrap
[auditing-err]     self.run()
[auditing-err]     ~~~~~~~~^^
[auditing-err]   File "C:\Python314\Lib\multiprocessing\process.py", line 108, in run
[auditing-err]     self._target(*self._args, **self._kwargs)
[auditing-err]     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
[auditing-err]     target(sockets=sockets)
[auditing-err]     ~~~~~~^^^^^^^^^^^^^^^^^
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 67, in run
[auditing-err]     return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
[auditing-err]   File "C:\Python314\Lib\asyncio\runners.py", line 204, in run
[auditing-err]     return runner.run(main)
[auditing-err]            ~~~~~~~~~~^^^^^^
[auditing-err]   File "C:\Python314\Lib\asyncio\runners.py", line 127, in run
[auditing-err]     return self._loop.run_until_complete(task)
[auditing-err]            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
[auditing-err]   File "C:\Python314\Lib\asyncio\base_events.py", line 719, in run_until_complete
[auditing-err]     return future.result()
[auditing-err]            ~~~~~~~~~~~~~^^
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 71, in serve
[auditing-err]     await self._serve(sockets)
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\server.py", line 78, in _serve
[auditing-err]     config.load()
[auditing-err]     ~~~~~~~~~~~^^
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\config.py", line 439, in load
[auditing-err]     self.loaded_app = import_from_string(self.app)
[auditing-err]                       ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
[auditing-err]     module = importlib.import_module(module_str)
[auditing-err]   File "C:\Python314\Lib\importlib\__init__.py", line 88, in import_module
[auditing-err]     return _bootstrap._gcd_import(name[level:], package, level)
[auditing-err]            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[auditing-err]   File "<frozen importlib._bootstrap>", line 1398, in _gcd_import
[auditing-err]   File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
[auditing-err]   File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
[auditing-err]   File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
[auditing-err]   File "<frozen importlib._bootstrap_external>", line 759, in exec_module
[auditing-err]   File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\auditing\app\main.py", line 3, in <module>
[auditing-err]     from .api import router as auditing_router
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\auditing\app\api.py", line 4, in <module>
[auditing-err]     from . import db, models, schemas, config
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\auditing\app\models.py", line 106, in <module>
[auditing-err]     class AuditEvent(Base):
[auditing-err]     ...<6 lines>...
[auditing-err]         metadata = Column(JSON)
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\decl_api.py", line 199, in __init__
[auditing-err]     _as_declarative(reg, cls, dict_)
[auditing-err]     ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 245, in _as_declarative
[auditing-err]     return _MapperConfig.setup_mapping(registry, cls, dict_, None, {})
[auditing-err]            ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 326, in setup_mapping
[auditing-err]     return _ClassScanMapperConfig(
[auditing-err]         registry, cls_, dict_, table, mapper_kw
[auditing-err]     )
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 573, in __init__
[auditing-err]     self._extract_mappable_attributes()
[auditing-err]     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
[auditing-err]   File "C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 1530, in _extract_mappable_attributes
[auditing-err]     raise exc.InvalidRequestError(
[auditing-err]     ...<2 lines>...
[auditing-err]     )
[auditing-err] sqlalchemy.exc.InvalidRequestError: Attribute name 'metadata' is reserved when using the Declarative API.
WARNING: auditing did not respond on port 8010 within timeout
Starting rmm on port 8020 (cwd=C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\core-services\rmm) using C:\Users\Matt.Palmer\Documents\GitHub\Tamsilcms-SIEM\venv\scripts\python.exe
[rmm-err] INFO:     Will watch for changes in these directories: ['C:\\Users\\Matt.Palmer\\Documents\\GitHub\\Tamsilcms-SIEM\\core-services\\rmm']
[rmm-err] INFO:     Uvicorn running on http://127.0.0.1:8020 (Press CTRL+C to quit)
[rmm-err] INFO:     Started reloader process [19340] using StatReload
[rmm-err] INFO:     Started server process [10584]
[rmm-err] INFO:     Waiting for application startup.
[rmm-err] INFO:     Application startup complete.
rmm is up on port 8020
