import re


# Class Args
#
# Schema description: # is for integer, * is for string, ## for double, [*] for varargs, default is boolean
#
# So a valid schema is: "a,b#,c*".
#
# With can then we retrieved:
# $args = new Args("a,b#,c*", arguments); // arguments = '-a true -b 1 -c "Hello"'
# $args.getB("a"); // Returns boolean
# $args.getI("b"); // Returns integer
# $args.getS("c"); // Returns String
#
# TODO:
# Refactor this code so it is easier to implement the getInteger functionality.
#
class Args:

    def __init__(self, formatToUse, arguments):
        """
         Construct a new instance of the Args class

         Parameters
         ----------
         formatToUse : str
             The format to use
         arguments : array
             The arguments to extract
         """

        self.formats = [format.strip() for format in formatToUse.split(',') if format.strip()]

        self.given_arguments = []
        self.boolean_arguments = {}
        self.string_arguments = {}

        self.split_arguments(arguments)

        if len(self.given_arguments) // 2 != len(self.formats):
            raise ParseException()

        for index, formatToUse in enumerate(self.formats):
            type_indicator = formatToUse[-1]

            if type_indicator == '*':
                value_from_arguments = self.given_arguments[index * 2 + 1]

                # exploded = re.split(r'"(.*?)"', valueFromArguments, 1)
                value_from_arguments = re.split(r'"(.*?)"', value_from_arguments, 2)

                if len(value_from_arguments) != 3:
                    raise ParseException()

                value_from_arguments = value_from_arguments[1]

                argument_key = formatToUse.strip('*')

                self.string_arguments[argument_key] = value_from_arguments
            else:
                value_from_arguments = self.given_arguments[index * 2 + 1]

                if value_from_arguments not in ['true', 'false']:
                    raise ParseException()

                value_from_arguments = value_from_arguments.lower() == 'true'

                self.boolean_arguments[formatToUse] = value_from_arguments

    def split_arguments(self, arguments):
        """
         Parse the arguments

         Parameters
         ----------
         arguments : array
             The arguments
         """

        splitted_arguments = [argument.strip() for argument in arguments.split('-') if argument.strip()]

        for argument_and_value in splitted_arguments:
            splitted = argument_and_value.split(' ', 1)

            argument_indicator = splitted[0].strip()
            argument_value = splitted[1].strip()

            self.given_arguments.append(argument_indicator)
            self.given_arguments.append(argument_value)

    # def rmQts(sinput):
    #     return sinput[index * 2 + 1].get(0)

    def getBoolean(self, key):
        """
         Get a boolean

         Parameters
         ----------
         key : the key
             The arguments

         Return
         ----------
         null if no entry is found, else boolean
         """

        return self.boolean_arguments.get(key)

    def getString(self, key):
        """
         Get a string

         Parameters
         ----------
         key : the key
             The arguments

         Return
         ----------
         null if no entry is found, else string
         """

        return self.string_arguments.get(key)


class ParseException(Exception):
    """
    Class ParseException

    Exception that gets thrown when something fails to parse properly
    """
    pass
