class Cal(object):
    def add_num_and_double(self, x, y):
        """Add and double
        >>> c = Cal()
        >>> c.add_num_and_double(1, 1)
        4

        >>> c.add_num_and_double('1', '1')
        Traceback (most recent call last):
        ...
        ValueError
        """
        if type(x) is not int or type(y) is not int:
            raise ValueError
        return (x + y) * 2


if __name__ == "__main__":
    import doctest
    doctest.testmod()
