__author__ = 'stephaneki'

from django.utils.html import escape


def html_to_content(h):
    return escape(h)