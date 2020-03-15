# -*- coding: utf-8 -*-

"""Documentation file twitter.py."""

# =============================================================================
# IMPORTS
# =============================================================================

from app.restplus import api
from flask_restplus import fields

# =============================================================================
# FUNCTIONS
# =============================================================================

def twitter_serializer():
    return api.model("Twitter",{
                "phrase": fields.String(required=True),
                "language": fields.String(required=True)
            })
