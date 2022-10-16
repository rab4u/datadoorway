from http import HTTPStatus


class DocStrings:
    COMMON_ENDPOINT_DOCS: dict = {
        HTTPStatus.UNAUTHORIZED.real: {
            "description": "Raises when unauthorized",
            "content": {
                "application/json": {
                    "example": {"Detail": "Exception raised while decoding JWT "
                                          "token. Insufficient permissions"}
                }
            }
        },
        HTTPStatus.FORBIDDEN.real: {
            "description": "Raises when unauthenticated",
            "content": {
                "application/json": {
                    "example": {"Detail": "Not Authenticated "}
                }
            }
        }
    }

    ROOT_ENDPOINT_DOCS: dict = {
        HTTPStatus.OK.real: {
            "description": "Intro message",
            "content": {
                "text/html": {
                    "example": "<H1> Data Doorway </H1>"
                }
            }
        }
    }

    PUBLISHER_GET_ENDPOINT_DOCS: dict = {
                                            HTTPStatus.OK.real: {
                                                "description": "Returns a json with list of publishers",
                                                "content": {
                                                    "application/json": {
                                                        "example": {"publishers": ["kafka", "s3", "bigquery"]}
                                                    }
                                                }
                                            }
                                        } | COMMON_ENDPOINT_DOCS

    PUBLISHER_POST_ENDPOINT_DOCS: dict = {
                                             HTTPStatus.OK.real: {
                                                 "description": "Sends the data to the publishers like kafka, s3, "
                                                                "gcs, ...",
                                                 "content": {
                                                     "application/json": {
                                                         "example": {"publishers": {
                                                             HTTPStatus.OK.real: ["kafka", "s3", "bigquery"],
                                                             HTTPStatus.INTERNAL_SERVER_ERROR: ["gcs", "athena"]
                                                         }}
                                                     }
                                                 }
                                             },
                                             HTTPStatus.UNPROCESSABLE_ENTITY.real: {
                                                 "description": "Raises when required parameters are missing",
                                                 "content": {
                                                     "application/json": {
                                                         "example": {"detail": [{
                                                             "loc": ["query", "publishers"],
                                                             "msg": "field required",
                                                             "type": "value_error.missing"
                                                         }]
                                                         }
                                                     }
                                                 }
                                             },
                                             HTTPStatus.BAD_REQUEST.real: {
                                                 "description": "Raises when required parameter values are incorrect",
                                                 "content": {
                                                     "application/json": {
                                                         "example": {
                                                             "detail": "Query param is invalid. Provide publisher "
                                                                       "values : {'string1'}. Allowed publisher "
                                                                       "values : {'console', 'file'} "
                                                         }
                                                     }
                                                 }
                                             }
                                         } | COMMON_ENDPOINT_DOCS

    ADMIN_GET_ENDPOINT_DOCS: dict = {
                                        HTTPStatus.OK.real: {
                                            "description": "Returns a json with list of settings",
                                            "content": {
                                                "application/json": {
                                                    "example": {
                                                        "settings": {
                                                            "security_enable_authorization": True,
                                                            "security_admin_secret": "**********",
                                                            "security_http_bearer_auto_error": False,
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        HTTPStatus.UNPROCESSABLE_ENTITY.real: {
                                            "description": "Raises when required header x-admin-secret is missing",
                                            "content": {
                                                "application/json": {
                                                    "example": {"detail": [{
                                                        "loc": ["query", "x-admin-secret"],
                                                        "msg": "field required",
                                                        "type": "value_error.missing"
                                                    }]
                                                    }
                                                }
                                            }
                                        },
                                    } | COMMON_ENDPOINT_DOCS

    ADMIN_PUT_ENDPOINT_DOCS: dict = {
                                        HTTPStatus.OK.real: {
                                            "description": "Returns a json with list of updated settings",
                                            "content": {
                                                "application/json": {
                                                    "example": {
                                                        "settings": {
                                                            "security_enable_authorization": True,
                                                            "security_admin_secret": "**********",
                                                            "security_http_bearer_auto_error": False,
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        HTTPStatus.UNPROCESSABLE_ENTITY.real: {
                                            "description": "Raises when required header x-admin-secret or payload is "
                                                           "missing",
                                            "content": {
                                                "application/json": {
                                                    "example": {"detail": [{
                                                        "loc": ["query", "x-admin-secret"],
                                                        "msg": "field required",
                                                        "type": "value_error.missing"
                                                    }]
                                                    }
                                                }
                                            }
                                        },
                                        HTTPStatus.BAD_REQUEST.real: {
                                            "description": "Raises when provided key is invalid",
                                            "content": {
                                                "application/json": {
                                                    "example": {
                                                        "detail": "Key 'string' not found in settings. 'Settings' "
                                                                  "object has no attribute 'string' "
                                                    }
                                                }
                                            }
                                        }
                                    } | COMMON_ENDPOINT_DOCS
