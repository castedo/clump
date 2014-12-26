find_program(PYTHON python)
set(PYINSTALL "${PYTHON} setup.py install --root=\$ENV{DESTDIR}")
install(CODE "execute_process(COMMAND ${PYINSTALL})")
