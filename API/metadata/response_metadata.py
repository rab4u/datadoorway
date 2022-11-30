from http import HTTPStatus


class ResponseMetadata:
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
                    "example": {"Detail": "Not Authenticated"}
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
                                             HTTPStatus.MULTI_STATUS.real: {
                                                 "description": "Sends the data to the publishers like kafka, s3, "
                                                                "gcs, ...",
                                                 "content": {
                                                     "application/json": {
                                                         "example": {
                                                             "success": {
                                                                 "kafka": {
                                                                     "status": 200,
                                                                     "destination": "mobile"
                                                                 }
                                                             },
                                                             "failed": {
                                                                 "s3": {
                                                                     "status": 500,
                                                                     "destination": "mobile"
                                                                 }
                                                             }
                                                         }
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

    SCHEMA_GET_ENDPOINT_DOCS: dict = {
                                         HTTPStatus.OK.real: {
                                             "description": "Returns the schema for specified schema_id",
                                             "content": {
                                                 "application/json": {
                                                     "example": {
                                                         "type": "object",
                                                         "properties": {
                                                             "name": {"type": "string", "minLength": 2,
                                                                      "maxLength": 50},
                                                             "age": {"type": "number", "minimum": 10,
                                                                     "exclusiveMaximum": 100},
                                                             "email": {"type": "string", "format": "email"},
                                                             "created_on": {"type": "string", "format": "date-time"},
                                                             "mobile_number": {"type": "string", "minLength": 9,
                                                                               "pattern": "^[0-9]*$"}
                                                         },
                                                         "required": ["age", "name", "email"]
                                                     }
                                                 }
                                             }
                                         },
                                         HTTPStatus.BAD_REQUEST.real: {
                                             "description": "Raises when provided schema_id is invalid "
                                                            "or when schema for schema id is not found",
                                             "content": {
                                                 "application/json": {
                                                     "example": {
                                                         "detail": "Query param is invalid. Allowed schema_id format "
                                                                   ": root/subject/name. Example: "
                                                                   "users/mobile/ios.json "
                                                     }
                                                 }
                                             }
                                         },
                                         HTTPStatus.UNPROCESSABLE_ENTITY.real: {
                                             "description": "Raises when required parameters are missing",
                                             "content": {
                                                 "application/json": {
                                                     "example": {"detail": [{
                                                         "loc": ["query", "schema_id"],
                                                         "msg": "field required",
                                                         "type": "value_error.missing"
                                                     }]
                                                     }
                                                 }
                                             }
                                         }
                                     } | COMMON_ENDPOINT_DOCS

    SCHEMA_POST_ENDPOINT_DOCS: dict = {
                                          HTTPStatus.OK.real: {
                                              "description": "Returns the success message",
                                              "content": {
                                                  "application/json": {
                                                      "example": {
                                                          "detail": "Successfully updated the schema with "
                                                                    "schema id: users/mobile/android"
                                                      }
                                                  }
                                              }
                                          },
                                          HTTPStatus.BAD_REQUEST.real: {
                                              "description": "Raises when provided schema_id is invalid",
                                              "content": {
                                                  "application/json": {
                                                      "example": {
                                                          "detail": "Query param is invalid. Allowed schema_id format "
                                                                    ": root/subject/name. Example: "
                                                                    "users/mobile/ios.json "
                                                      }
                                                  }
                                              }
                                          },
                                          HTTPStatus.UNPROCESSABLE_ENTITY.real: {
                                              "description": "Raises when required parameters are missing",
                                              "content": {
                                                  "application/json": {
                                                      "example": {"detail": [{
                                                          "loc": ["query", "schema_id"],
                                                          "msg": "field required",
                                                          "type": "value_error.missing"
                                                      }]
                                                      }
                                                  }
                                              }
                                          }
                                      } | COMMON_ENDPOINT_DOCS

    SCHEMA_VALIDATE_ENDPOINT_DOCS: dict = {
                                      HTTPStatus.OK.real: {
                                          "description": "Returns the success message",
                                          "content": {
                                              "application/json": {
                                                  "example": {
                                                      "detail": "Schema validation is successful"
                                                  }
                                              }
                                          }
                                      },
                                      HTTPStatus.BAD_REQUEST.real: {
                                          "description": "Raises when schema or data is invalid",
                                          "content": {
                                              "application/json": {
                                                  "example": {
                                                      "detail": "Data Validation failed. reason: 100 is "
                                                                "greater than or equal to the maximum of 100 "
                                                  }
                                              }
                                          }
                                      },
                                      HTTPStatus.UNPROCESSABLE_ENTITY.real: {
                                          "description": "Raises when required body params are missing",
                                          "content": {
                                              "application/json": {
                                                  "example": {
                                                      "detail": [
                                                          {
                                                              "loc": [
                                                                  "body",
                                                                  "json_schema"
                                                              ],
                                                              "msg": "field required",
                                                              "type": "value_error.missing"
                                                          }
                                                      ]
                                                  }
                                              }
                                          }
                                      }
                                  } | COMMON_ENDPOINT_DOCS
