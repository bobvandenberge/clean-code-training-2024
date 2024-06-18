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

    def __init__(self, fmt, args):
        """
         Construct a new instance of the Args class

         Parameters
         ----------
         fmt : str
             The format to use
         args : array
             The arguments to extract
         """

        self.array_fmt = [f.strip() for f in fmt.split(',') if f.strip()]
        """The format that needs to be checked"""

        self.array_args = []
        """The arguments that were given"""

        self.array_bools = {}
        """The variable in which the booleans get stored"""

        self.array_strs = {}
        """The variable in which the strings get stored"""

        self.prs_args(args)

        if len(self.array_args) // 2 != len(self.array_fmt):
            raise ParseException()

        for index, fmt in enumerate(self.array_fmt):
            type_indicator = fmt[-1]

            if type_indicator == '*':
                v = self.array_args[index * 2 + 1]  # Value from arguments

                # exploded = re.split(r'"(.*?)"', v, 1)
                exploded = re.split(r'"(.*?)"', v, 2)

                if len(exploded) != 3:
                    raise ParseException()

                val = exploded[1]

                index_fmt = fmt.strip('*')

                self.array_strs[index_fmt] = val
            else:
                v = self.array_args[index * 2 + 1]  # Value from arguments

                if v not in ['true', 'false']:
                    raise ParseException()

                val = v.lower() == 'true'

                self.array_bools[fmt] = val

    def prs_args(self, args):
        """
         Parse the arguments

         Parameters
         ----------
         args : array
             The arguments
         """

        tmp = [arg.strip() for arg in args.split('-') if arg.strip()]

        for arg in tmp:
            exploded = arg.split(' ', 1)
            self.array_args.append(exploded[0].strip())
            self.array_args.append(exploded[1].strip())

    # def rmQts(sinput):
    #     return sinput[index * 2 + 1].get(0)

    def getB(self, k):
        """
         Get a boolean

         Parameters
         ----------
         k : the key
             The arguments

         Return
         ----------
         null if no entry is found, else boolean
         """

        return self.array_bools.get(k)

    def getS(self, k):
        """
         Get a string

         Parameters
         ----------
         k : the key
             The arguments

         Return
         ----------
         null if no entry is found, else string
         """

        return self.array_strs.get(k)


class ParseException(Exception):
    """
    Class ParseException

    Exception that gets thrown when something fails to parse properly
    """
    pass
