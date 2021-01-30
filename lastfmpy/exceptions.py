"""
MIT License

Copyright (c) 2020 Myer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class InvalidInputError(Exception):
    """
    API error code 6
    The exception raised when a request to the API resulted in nothing being found
    """

    def __init__(self, message):
        self.message = message


class ServiceOfflineError(Exception):
    """
    API error code 11
    The exception raised when a request to the API errored because the service was offline
    """

    def __init__(self, message):
        self.message = message


class TemporaryError(Exception):
    """
    API error code 29
    The exception raised when a request to the API errored because the service was temporarily unavailable
    """

    def __init__(self, message):
        self.message = message


class RatelimitExceededError(Exception):
    def __init__(self, message):
        self.message = message
