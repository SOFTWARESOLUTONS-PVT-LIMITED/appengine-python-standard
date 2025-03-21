#!/usr/bin/env python
#
# Copyright 2007 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Save X-Appengine-* headers into request context."""
import contextvars
from typing import Dict

PREFIX = 'HTTP_X_APPENGINE_'

AUTH_DOMAIN = contextvars.ContextVar('AUTH_DOMAIN')
DEFAULT_VERSION_HOSTNAME = contextvars.ContextVar('DEFAULT_VERSION_HOSTNAME')
USER_EMAIL = contextvars.ContextVar('USER_EMAIL')
USER_ID = contextvars.ContextVar('USER_ID')
USER_IS_ADMIN = contextvars.ContextVar('USER_IS_ADMIN')
USER_NICKNAME = contextvars.ContextVar('USER_NICKNAME')
DEFAULT_NAMESPACE = contextvars.ContextVar('DEFAULT_NAMESPACE')


def init_from_wsgi_environ(
    wsgi_env) -> Dict[contextvars.ContextVar, contextvars.Token]:
  """Init contextvars from matching X_APPENGINE_ headers if found."""

  reset_tokens: Dict[contextvars.ContextVar, contextvars.Token] = {}
  for ctxvar in [v for _, v in globals().items()
                 if isinstance(v, contextvars.ContextVar)]:
    value = wsgi_env.get(PREFIX + ctxvar.name)
    if value is not None:
      if ctxvar.name == 'USER_IS_ADMIN':

        value = (value == '1')
      token = ctxvar.set(value)
      reset_tokens[ctxvar] = token
  return reset_tokens
