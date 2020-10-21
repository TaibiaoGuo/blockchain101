.. currentmodule:: dialog

pythondialog-specific exceptions
================================

Class hierarchy
---------------

Here is the hierarchy of notable exceptions raised by this module:

| :exc:`error`
|    :exc:`ExecutableNotFound`
|    :exc:`BadPythonDialogUsage`
|    :exc:`PythonDialogSystemError`
|       :exc:`PythonDialogOSError`
|          :exc:`PythonDialogIOError`  (should not be raised starting from
                                        Python 3.3, as :exc:`IOError` becomes
                                        an alias of :exc:`OSError`)
|       :exc:`PythonDialogErrorBeforeExecInChildProcess`
|       :exc:`PythonDialogReModuleError`
|    :exc:`UnexpectedDialogOutput`
|    :exc:`DialogTerminatedBySignal`
|    :exc:`DialogError`
|    :exc:`UnableToRetrieveBackendVersion`
|    :exc:`UnableToParseBackendVersion`
|       :exc:`UnableToParseDialogBackendVersion`
|    :exc:`InadequateBackendVersion`
|    :exc:`PythonDialogBug`
|    :exc:`ProbablyPythonBug`

As you can see, every exception *exc* among them verifies::

  issubclass(exc, error)

so if you don't need fine-grained error handling, simply catch :exc:`error`
(which will probably be accessible as :exc:`dialog.error` from your program)
and you should be safe.

.. versionchanged:: 2.12
   :exc:`PythonDialogIOError` is now a subclass of :exc:`PythonDialogOSError`
   in order to help with the transition from :exc:`IOError` to :exc:`OSError`
   in the Python language. With this change, you can safely replace ``except
   PythonDialogIOError`` clauses with ``except PythonDialogOSError`` even if
   running under Python < 3.3.


Detailed list
-------------

.. autoexception:: error

.. autoexception:: ExecutableNotFound
   :show-inheritance:

.. autoexception:: BadPythonDialogUsage
   :show-inheritance:

.. autoexception:: PythonDialogSystemError
   :show-inheritance:

.. autoexception:: PythonDialogOSError
   :show-inheritance:

.. autoexception:: PythonDialogIOError
   :show-inheritance:

.. autoexception:: PythonDialogErrorBeforeExecInChildProcess
   :show-inheritance:

.. autoexception:: PythonDialogReModuleError
   :show-inheritance:

.. autoexception:: UnexpectedDialogOutput
   :show-inheritance:

.. autoexception:: DialogTerminatedBySignal
   :show-inheritance:

.. autoexception:: DialogError
   :show-inheritance:

.. autoexception:: UnableToRetrieveBackendVersion
   :show-inheritance:

.. autoexception:: UnableToParseBackendVersion
   :show-inheritance:

.. autoexception:: UnableToParseDialogBackendVersion
   :show-inheritance:

.. autoexception:: InadequateBackendVersion
   :show-inheritance:

.. autoexception:: PythonDialogBug
   :show-inheritance:

.. autoexception:: ProbablyPythonBug
   :show-inheritance:
