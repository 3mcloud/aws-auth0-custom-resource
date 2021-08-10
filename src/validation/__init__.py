"""
Schema validation
"""
import stringcase
from cerberus import Validator


def to_bool(val):
    """Return a bool version of val"""
    if isinstance(val, bool):
        return val
    return val in ['true', 'True']


class AuthnValidator(Validator):
    """
    Validator primitives for muxing cloudformation into
    valid api calls and ensuring the values are correct
    """
    def __init__(self, schema, *args, with_defaults=None, **kwargs):
        super().__init__(schema, *args, **kwargs)
        self.with_defaults = with_defaults

    def validated(  # pylint: disable=too-many-arguments, arguments-differ
            self,
            document,
            schema=None,
            update=False,
            normalize=True,
            always_return_document=False,
    ):
        """ overload internal validated to change the order of operations"""
        if schema is None:
            schema = self.schema
        document = self.normalize_document(document)
        if normalize:
            # Purge readonly
            for field in [x for x in document if schema.get(x, {}).get('readonly', False)]:
                document.pop(field)
            # Coerce
            self.coerce_mapping(document, schema)
        document = super().validated(document, schema=schema, update=update, normalize=False,
                                     always_return_document=always_return_document)
        if document is None:
            return document
        if normalize:
            # Purge unknown before we normalize
            for field in [x for x in document if x not in schema]:
                document.pop(field)
            normalized = self.normalized(document, schema)
            return self.apply_defaults(normalized)

        return self.apply_defaults(document)
        # return document

    def apply_defaults(self, document):
        """
        if self.with_defaults then apply the default values
        DOES NOT support normalization. This is called after
        normalization has happened. Any defaults need to be the
        coerced names/values of the schema.
        """
        if not self.with_defaults or not callable(self.with_defaults):
            return document

        return {**self.with_defaults(document), **document}

    def coerce_mapping(self, mapping, schema):
        """Follow all the coersions in a mapping, recursively"""
        self._normalize_coerce(mapping, schema)
        for field in mapping:
            if isinstance(mapping[field], dict) and 'schema' in schema[field]:
                self.coerce_mapping(mapping[field], schema[field]['schema'])

    def normalize_document(self, document):
        """
        convert all input keys to snakecase
        """
        out = None
        if isinstance(document, dict):
            out = {}
            for key, value in document.items():
                out[stringcase.snakecase(key)] = self.normalize_document(value)
            return out
        if isinstance(document, list):
            out = []
            for value in document:
                out.append(self.normalize_document(value))
            return out
        return document

    def _validate_isodd(self, isodd, field, value):
        """ Test the oddity of a value.

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if isodd and not bool(value & 1):
            self._error(field, "Must be an odd number")
