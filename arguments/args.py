import re

STRING_TYPE = '*'
INTEGER_TYPE = '#'
DOUBLE_TYPE = '##'
BOOLEAN_TYPE = ''

# Class Args
#
# Schema type indicators: # is for integer, * is for string, ## for double, [*] for varargs, default is boolean
#
# So a valid schema is: "a,b#,c*".
#
# With can then we retrieved:
# $args = new Args("a,b#,c*", arguments); // arguments = '-a true -b 1 -c "Hello"'
# $args.getB("a"); // Returns boolean
# $args.getI("b"); // Returns integer
# $args.getS("c"); // Returns String
class Args:

    def __init__(self, schema, arguments):
        self.schema_parts = [schema_part.strip() for schema_part in schema.split(',') if schema_part.strip()]

        self.supplied_arguments = self.split_arguments(arguments)
        self.boolean_arguments = {}
        self.string_arguments = {}

        if not self.are_mandatory_arguments_present(self.schema_parts, self.supplied_arguments):
            raise ParseException()

        for index, schema_part in enumerate(self.schema_parts):
            type_indicator = schema_part[-1]

            if type_indicator == STRING_TYPE:
                self.parse_as_string(index, schema_part)
            else:
                self.parse_as_boolean(index, schema_part)

    def parse_as_boolean(self, index, schema_part):
        argument_value_part = self.supplied_arguments[index * 2 + 1]

        if argument_value_part not in ['true', 'false']:
            raise ParseException()

        argument_value = argument_value_part.lower() == 'true'

        self.boolean_arguments[schema_part] = argument_value

    def parse_as_string(self, index, schema_part):
        argument_value_part = self.supplied_arguments[index * 2 + 1]

        argument_value_splitted = re.split(r'"(.*?)"', argument_value_part, 2)

        if len(argument_value_splitted) != 3:
            raise ParseException()

        argument_value = argument_value_splitted[1]

        argument_key = schema_part.strip('*')

        self.string_arguments[argument_key] = argument_value

    def are_mandatory_arguments_present(self, formats, supplied_arguments):
        return len(supplied_arguments) // 2 == len(formats)

    def split_arguments(self, arguments):
        argument_parts = [argument.strip() for argument in arguments.split('-') if argument.strip()]
        all_parts = []

        for argument_part in argument_parts:
            splitted_argument_part = argument_part.split(' ', 1)

            argument_indicator = splitted_argument_part[0].strip()
            all_parts.append(argument_indicator)

            argument_value = splitted_argument_part[1].strip()
            all_parts.append(argument_value)

        return all_parts

    def get_boolean(self, key):
        return self.boolean_arguments.get(key)

    def get_string(self, key):
        return self.string_arguments.get(key)


class ParseException(Exception):
    """
    Class ParseException

    Exception that gets thrown when something fails to parse properly
    """
    pass
