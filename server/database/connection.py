"""
Salamander ALM
Copyright (c) 2016  Djuro Drljaca

This Python module is free software; you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation; either version 2 of the
License, or (at your option) any later version.

This Python module is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this library. If
not, see <http://www.gnu.org/licenses/>.
"""


class Connection(object):
    """
    Base class for a database connection
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def __del__(self):
        """
        Destructor
        """
        pass

    @property
    def in_transaction(self) -> bool:
        """
        Checks if a transaction is active on the connection

        :return:    Transaction is active or not
        """
        raise NotImplementedError()

    def begin_transaction(self) -> bool:
        """
        Begins a transaction

        :return:    Success or failure
        """
        raise NotImplementedError()

    def commit_transaction(self) -> bool:
        """
        Commits the currently active transaction

        :return:    Success or failure
        """
        raise NotImplementedError()

    def rollback_transaction(self) -> bool:
        """
        Rolls back the currently active transaction

        :return:    Success or failure
        """
        raise NotImplementedError()
