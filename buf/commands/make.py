# File name: make.py
# Author: Jordan Juravsky
# Date created: 31-07-2018


from buf.commands import chemical, recipe


from sys import exit


def make(options):
    if options["<recipe_name>"]:
        recipe_object = get_recipe(options["<recipe_name>"])
    else:
        recipe_object = recipe.make_safe_recipe("", options["<concentration>"], options["<chemical_name>"], recipe_library= {})

    buffer_volume_in_litres = get_buffer_litres(options["<volume>"])

    buffer = BufferInstructions(buffer_volume_in_litres, recipe_object)
    buffer.print()


def get_buffer_litres(volume_as_string):
    quantity, unit = recipe.split_concentration(volume_as_string)

    try:
        quantity = float(quantity)
    except:
        print(f"Invalid quantity: '{quantity}' is not a valid number.")
        exit()

    if unit not in recipe.volume_units:
        print(f"Invalid unit: '{unit}' is not a valid unit of volume.")
        exit()

    return quantity * recipe.volume_units_to_litres[unit]


def calculate_amount_to_add(buffer_volume_in_litres, chemical_object, concentration):
    quantity, unit = recipe.split_concentration(concentration)

    # Try/catch this?
    quantity = float(quantity)

    # TODO: make sure unit is valid?

    if unit in recipe.volume_units or unit in recipe.mass_units:
        return concentration
    elif unit in recipe.concentration_units:
        # TODO: convert to mg if number is small.
        return str(quantity * recipe.concentration_units[unit] * chemical_object.molar_mass * buffer_volume_in_litres) + "g"
    elif unit == "%":
        # TODO: accomodate non-litre volume units.
        return str(quantity / 100 * buffer_volume_in_litres) + "L"

def get_recipe(recipe_name):
    recipe_library = recipe.load_recipes()

    if recipe_name not in recipe_library:
        # TODO: prompt user to add it.
        # TODO: make a module to handle errors like these.
        print(f"Invalid recipe name: '{recipe_name}' not found in chemical library")
        exit()

    return recipe_library[recipe_name]


class Step:
    def __init__(self, name, concentration, amount_to_add):
        self.name = name
        self.concentration = concentration
        self.amount_to_add = amount_to_add

class BufferInstructions:

    def __init__(self, buffer_volume_in_litres, recipe_object):

        self.steps = []

        chemicals = chemical.load_chemicals()

        for concentration, chemical_name in zip(recipe_object.concentrations, recipe_object.chemical_names):
            self.steps.append(Step(chemical_name, concentration, calculate_amount_to_add(concentration)))

        # TODO: sort the steps in some way (need to implement in Step class first).

    def print(self):
        matrix = [[step.name, step.concentration, step.amount_to_add] for step in self.steps]

        print_table(matrix, header = ["Chemical Name", "Concentration", "Amount to Add"])

# Courtesy of jhcepas: https://gist.github.com/jhcepas/5884168
def print_table(items, header=None, wrap=True, max_col_width=20, wrap_style="wrap", row_line=False,
                fix_col_width=False):
    ''' Prints a matrix of data as a human readable table. Matrix
    should be a list of lists containing any type of values that can
    be converted into text strings.
    Two different column adjustment methods are supported through
    the *wrap_style* argument:

       wrap: it will wrap values to fit max_col_width (by extending cell height)
       cut: it will strip values to max_col_width
    If the *wrap* argument is set to False, column widths are set to fit all
    values in each column.
    This code is free software. Updates can be found at
    https://gist.github.com/jhcepas/5884168

    '''

    if fix_col_width:
        c2maxw = dict([(i, max_col_width) for i in xrange(len(items[0]))])
        wrap = True
    elif not wrap:
        c2maxw = dict([(i, max([len(str(e[i])) for e in items])) for i in xrange(len(items[0]))])
    else:
        c2maxw = dict([(i, min(max_col_width, max([len(str(e[i])) for e in items])))
                       for i in xrange(len(items[0]))])
    if header:
        current_item = -1
        row = header
        if wrap and not fix_col_width:
            for col, maxw in c2maxw.iteritems():
                c2maxw[col] = max(maxw, len(header[col]))
                if wrap:
                    c2maxw[col] = min(c2maxw[col], max_col_width)
    else:
        current_item = 0
        row = items[current_item]
    while row:
        is_extra = False
        values = []
        extra_line = [""] * len(row)
        for col, val in enumerate(row):
            cwidth = c2maxw[col]
            wrap_width = cwidth
            val = str(val)
            try:
                newline_i = val.index("\n")
            except ValueError:
                pass
            else:
                wrap_width = min(newline_i + 1, wrap_width)
                val = val.replace("\n", " ", 1)
            if wrap and len(val) > wrap_width:
                if wrap_style == "cut":
                    val = val[:wrap_width - 1] + "+"
                elif wrap_style == "wrap":
                    extra_line[col] = val[wrap_width:]
                    val = val[:wrap_width]
            val = val.ljust(cwidth)
            values.append(val)
        print
        ' | '.join(values)
        if not set(extra_line) - set(['']):
            if header and current_item == -1:
                print
                ' | '.join(['=' * c2maxw[col] for col in xrange(len(row))])
            current_item += 1
            try:
                row = items[current_item]
            except IndexError:
                row = None
        else:
            row = extra_line
            is_extra = True

        if row_line and not is_extra and not (header and current_item == 0):
            if row:
                print
                ' | '.join(['-' * c2maxw[col] for col in xrange(len(row))])
            else:
                print
                ' | '.join(['=' * c2maxw[col] for col in xrange(len(extra_line))])
