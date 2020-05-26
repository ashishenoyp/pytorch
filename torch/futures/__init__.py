"""
The ``torch.futures`` package contains a ``Future`` type and corresponding
utility functions.
"""
import torch


class Future(torch._C.Future):
    r"""
    Wrapper around a ``torch._C.Future``.
    """
    def __new__(cls):
        return super(Future, cls).__new__(cls)

    def wait(self):
        r"""
        Block until the value of this ``Future`` is ready.

        Return:
            The value held by this ``Future``.
        """
        return super(Future, self).wait()

    def then(self, callback):
        r"""
        Append the given callback function to this ``Future``, which will be run
        when the ``Future`` is completed.  Multiple callbacks can be added to
        the same ``Future``, and will be invoked in the same order as they were
        added. The callback must take one argument, which is the reference to
        this ``Future``. The callback function can use the ``Future.wait()`` API
        to get the value.

        Argument:
            callback(``Callable``): a ``Callable`` that takes this ``Future`` as
                                    the only argument.

        Return:
            A new ``Future`` object that holds the return value of the
            ``callback`` and will be marked as completed when the given
            ``callback`` finishes.

        Example::
            >>> import torch
            >>>
            >>> def callback(fut):
            >>>     print(f"RPC return value is {fut.wait()}.")
            >>>
            >>> fut = torch.futures.Future()
            >>> # The inserted callback will print the return value when
            >>> # receiving the response from "worker1"
            >>> cb_fut = fut.then(callback)
            >>> chain_cb_fut = cb_fut.then(lambda x : print(f"Chained cb done. {x.wait()}"))
            >>> fut.set_result(5)
            >>>
            >>> # Outputs are:
            >>> # RPC return value is 5.
            >>> # Chained cb done. None
        """
        return super(Future, self).then(callback)

    def set_result(self, result):
        r"""
        Set the result for this ``Future``, which will mark this ``Future`` as
        completed and trigger all attached callbacks. Note that a ``Future``
        cannot be marked completed twice.

        Arguments:
            result (object): the result object of this ``Future``.

        Example::
            >>> from torch.distributed import rpc
            >>> import torch
            >>>
            >>> fut = rpc.Future()
            >>> rpc_fut = rpc.async(
            >>>     "worker1",
            >>>     torch.add,
            >>>     args=(torch.ones(2), 1)
            >>> )
            >>> rpc_fut.add_done_callback(
            >>>     lambda rpc_fut : fut.set_result(rpc_fut.wait() + 1)
            >>> )
            >>> print(fut.wait())  # tensor([3., 3.])
        """
        super(Future, self).set_result(result)
