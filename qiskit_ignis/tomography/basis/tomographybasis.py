# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
TomographyBasis class
"""

from qiskit import QuantumRegister
from qiskit import ClassicalRegister
from qiskit import QISKitError


class TomographyBasis(object):
    """
    Tomography basis class.
    """

    def __init__(self, name, measurement=None, preparation=None):

        # TODO: check that measurement and preparation are both tuples
        # (labels, circuit_fn, matrix_fn)
        # Also check functions have correct signature and are return valid
        # outputs for all specified labels

        self._name = name
        self._measurement = False
        self._preparation = False

        if measurement is not None and len(measurement) == 3:
            self._measurement = True
            self._measurement_labels = measurement[0]
            self._measurement_circuit = measurement[1]
            self._measurement_matrix = measurement[2]

        if preparation is not None and len(preparation) == 3:
            self._preparation = True
            self._preparation_labels = preparation[0]
            self._preparation_circuit = preparation[1]
            self._preparation_matrix = preparation[2]

    @property
    def name(self):
        return self._name

    @property
    def measurement(self):
        return self._measurement

    @property
    def preparation(self):
        return self._preparation

    @property
    def measurement_labels(self):
        if self.measurement is True:
            return self._measurement_labels
        return None

    @property
    def preparation_labels(self):
        if self.preparation is True:
            return self._preparation_labels
        return None

    def measurement_circuit(self, op, qubit, clbit):
        # Error Checking
        if self.measurement is False:
            raise QISKitError("{} is not a measurement basis".format(self._name))

        if not (isinstance(qubit, tuple) and isinstance(qubit[0], QuantumRegister)):
            raise QISKitError('Input must be a qubit in a QuantumRegister')

        if not (isinstance(clbit, tuple) and isinstance(clbit[0], ClassicalRegister)):
            raise QISKitError('Input must be a bit in a ClassicalRegister')

        if op not in self._measurement_labels:
            msg = "Invalid {0} measurement operator label".format(self._name)
            error = "'{0}' != {1}".format(op, self._measurement_labels)
            raise ValueError("{0}: {1}".format(msg, error))

        # Return QuantumCircuit function output
        return self._measurement_circuit(op, qubit, clbit)

    def preparation_circuit(self, op, qubit):

        # Error Checking
        if self.preparation is False:
            raise QISKitError("{} is not a preparation basis".format(self._name))

        if not (isinstance(qubit, tuple) and isinstance(qubit[0], QuantumRegister)):
            raise QISKitError('Input must be a qubit in a QuantumRegister')

        if op not in self._preparation_labels:
            msg = "Invalid {0} preparation operator label".format(self._name)
            error = "'{}' not in {}".format(op, self._preparation_labels)
            raise ValueError("{0}: {1}".format(msg, error))

        return self._preparation_circuit(op, qubit)

    def measurement_matrix(self, label, outcome):

        if self.measurement is False:
            raise QISKitError("{} is not a measurement basis".format(self._name))

        # Check input is valid for this basis
        if label not in self._measurement_labels:
            msg = "Invalid {0} measurement operator label".format(self._name)
            error = "'{}' not in {}".format(label, self._measurement_labels)
            raise ValueError("{0}: {1}".format(msg, error))

        # Check outcome is valid for this measurement
        allowed_outcomes = [0, 1, '0', '1']
        if outcome not in allowed_outcomes:
            error = "'{}' not in {}".format(outcome, allowed_outcomes)
            raise ValueError('Invalid measurement outcome: {}'.format(error))

        return self._measurement_matrix(label, outcome)

    def preparation_matrix(self, label):

        if self.preparation is False:
            raise QISKitError("{} is not a preparation basis".format(self._name))

        # Check input is valid for this basis
        if label not in self._preparation_labels:
            msg = "Invalid {0} preparation operator label".format(self._name)
            error = "'{}' not in {}".format(label, self._preparation_labels)
            raise ValueError("{0}: {1}".format(msg, error))

        return self._preparation_matrix(label)
