from cx_Freeze import setup, Executable

build_exe_options = {"packages": ['os', 'cffi', 'idna']}


setup(name="freeradius user management",
      version="0.1",
      description="Software for user management in freeRadius",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base="Win32GUI")])