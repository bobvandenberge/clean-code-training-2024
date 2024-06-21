import re

class ParseException(Exception):
    """Exception thrown when parsing fails."""
    pass


class Args:
    def __init__(self, fmt, args):
        """
        Construct a new instance of the Args class.

        Parameters
        ----------
        fmt : str
            The format to use.
        args : str
            The arguments to extract.
        """
        self.schema = self.parse_schema(fmt)
        self.args = self.parse_args(args)
        self.boolean_args = {}
        self.string_args = {}
        self.process_arguments()

    def parse_schema(self, fmt):
        """
        Parse the schema format.

        Parameters
        ----------
        fmt : str
            The format to use.

        Returns
        -------
        list
            List of schema elements.
        """
        return [f.strip() for f in fmt.split(',') if f.strip()]

    def parse_args(self, args):
        """
        Parse the arguments.

        Parameters
        ----------
        args : str
            The arguments.

        Returns
        -------
        list
            List of parsed arguments.
        """
        parsed_args = []
        tmp_args = [arg.strip() for arg in args.split('-') if arg.strip()]
        for arg in tmp_args:
            key, value = arg.split(' ', 1)
            parsed_args.append((key.strip(), value.strip()))
        return parsed_args

    def process_arguments(self):
        """
        Process the arguments based on the schema.
        """
        if len(self.args) != len(self.schema):
            raise ParseException()

        for (key, value), schema in zip(self.args, self.schema):
            type_indicator = schema[-1]
            key = schema[:-1]

            if type_indicator == '*':
                self.string_args[key] = self.extract_string(value)
            elif type_indicator == '#':
                self.boolean_args[key] = self.extract_boolean(value)
            else:
                raise ParseException()

    def extract_string(self, value):
        """
        Extract a string value from the arguments.

        Parameters
        ----------
        value : str
            The argument value.

        Returns
        -------
        str
            The extracted string.
        """
        exploded = re.split(r'"(.*?)"', value, 2)
        if len(exploded) != 3:
            raise ParseException()
        return exploded[1]

    def extract_boolean(self, value):
        """
        Extract a boolean value from the arguments.

        Parameters
        ----------
        value : str
            The argument value.

        Returns
        -------
        bool
            The extracted boolean.
        """
        if value.lower() not in ['true', 'false']:
            raise ParseException()
        return value.lower() == 'true'

    def get_boolean(self, key):
        """
        Get a boolean value.

        Parameters
        ----------
        key : str
            The key for the boolean value.

        Returns
        -------
        bool
            The boolean value.
        """
        return self.boolean_args.get(key)

    def get_string(self, key):
        """
        Get a string value.

        Parameters
        ----------
        key : str
            The key for the string value.

        Returns
        -------
        str
            The string value.
        """
        return self.string_args.get(key)
