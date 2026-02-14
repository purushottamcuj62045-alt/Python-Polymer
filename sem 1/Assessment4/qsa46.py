""""Write a function called add_all_nums which takes arbitrary number of arguments and sums all the arguments.
 Check if all the list items are number types. If not do give a reasonable feedback."""
def add_all_nums(*args):
    total = 0
    for num in args:
        if isinstance(num, (int, float)):
            total += num
        else:
            return "Error: All arguments must be numbers."
    return total
print("sum of all nums",add_all_nums(5,8,9))