from collections import namedtuple
import copy

Customer = namedtuple('Customer', 'name order')

Store = namedtuple('Store', 'name inventory')

customer_totals = {}


def get_avg(inventory):
    """Get the average."""
    price_sum = 0
    quantity = 0

    for j in inventory:
        price_sum += inventory[j][0] * inventory[j][1]
        quantity += inventory[j][1]
    return price_sum / quantity


def get_orders(customer):
    """Get the order from a customer."""
    name = customer.name
    order = customer.order
    sorted_list = sorted(order)
    order_string = name + ' wants'

    if order:
        # when this person wants something

        for i in sorted_list:

            order_name = i
            order_num = order[order_name]

            if i == sorted_list[-1]:
                # dealing with the period
                order_string += ' {} {}.'.format(order_num, order_name)
            else:
                # dealing with the comma
                order_string += ' {} {},'.format(order_num, order_name)
    else:
        # when this person does not want anything
        order_string = name + ' does not want anything.'

    return (order_string, sorted_list)


def order_check(order, order_name, customer_name):
    """Check the if the order is satisfied and print unsatisfied results."""
    for i in order:
        remain_num = order[i]
        if order_name == i and remain_num > 0:
            print('    All stores were sold out of {0}; {1} could not'
                  ' purchase {2} {0}'.format(order_name, customer_name, remain_num))
            break


def produce_receipt(customer_name, store_name, expense):
    """Produce the receipt after a purchase."""
    name = customer_name
    if name not in customer_totals:
        # add the customer to the receipt
        customer_totals[name] = dict()
        # initialize the expense value
        customer_totals[name][store_name] = 0
        customer_totals[name][store_name] += expense
    else:
        # add the store name and expense
        if store_name not in customer_totals[name]:

            # initialize the expense value
            customer_totals[name][store_name] = 0
            customer_totals[name][store_name] += expense
        else:
            customer_totals[name][store_name] += expense


def purchase(customer, stores):
    """Make the purchase."""
    name = customer.name
    sorted_list = get_orders(customer)[1]
    order = customer.order

    for i in sorted_list:
        # check every object on the order list

        order_name = i
        order_num = order[order_name]

        for store in stores:
            # check every store

            store_name = store.name
            inventory = store.inventory
            expense = 0

            if order_name in inventory:
                # this store has the object in stock
                in_stock = inventory[order_name][1]
                price = inventory[order_name][0]

                if 0 < order_num <= in_stock:
                    # enough stock

                    # reduce stocks
                    inventory[order_name][1] -= order_num

                    # reduce order quantities
                    order[order_name] = 0
                    expense = price * order_num

                    output_string = '    Purchased {} {} at {} for ${:.2f}'.format(order_num, order_name,
                                                                                   store_name, expense)
                    order_num = 0
                    print(output_string)
                elif order_num > in_stock > 0:
                    # not enough stock

                    # reduce order quantities
                    order[order_name] -= inventory[order_name][1]
                    remain_num = inventory[order_name][1]

                    # empty the stock
                    # del inventory[order_name]
                    inventory[order_name][1] = 0

                    expense = price * remain_num

                    output_string = '    Purchased {} {} at {} for ${:.2f}'.format(remain_num, order_name,
                                                                                   store_name, expense)
                    print(output_string)
                else:

                    pass
            else:
                # this store does NOT has the object in stock
                pass

            # produce the receipt after each visiting each store
            # print('Expense', expense)
            produce_receipt(name, store_name, expense)

        # check if current object is sold out
        order_check(order, order_name, name)


def part_one(stores):
    """Part one."""
    prev_avg = 0
    stores.reverse()

    for i in stores:

        avg = get_avg(i.inventory)
        print('The average item at {} costs ${:.2f}'.format(i.name, avg))

        if prev_avg > avg:
            print('Error: Outdated information, quitting program...')
            return
        prev_avg = avg


def part_two_and_three(customers, stores):
    """Part two and three."""
    for customer in customers:
        order = customer.order
        print(get_orders(customer)[0])

        if order:
            purchase(customer, stores)
        else:
            pass


def part_three(customers, stores):
    """Part three (unused)."""
    for customer in customers:
        order = customer.order

        if order:
            purchase(customer, stores)
        else:
            pass


def drone_delivery_service(customers, stores):
    """
    Print Instructions for Drone Delivery Service.

    :param customers: [Customer(str, {str: float})]
    :param stores: [Store(str, {str: [float, int]})]
    """
    stores_copy = copy.deepcopy(stores)
    part_one(stores_copy)
    print()
    part_two_and_three(customers, stores_copy)
    # reverse it back
    stores_copy.reverse()
    stores = stores_copy
    return customer_totals, stores


if __name__ == '__main__':
    # Set submit_mode to False to be able to run this code in python tutor or development mode
    # Ensure it is set to True when submitting code
    submit_mode = True
    if submit_mode:
        drone_delivery_service(*eval(input()))
    else:
        print("THIS IS A TEST RUN - IF YOU ARE SEEING "
              "THIS IN SUBMIT MODE, SET submit_mode = True AND RERUN")
        drone_delivery_service(
            [
                Customer(name='One', order={'a': 10, 'b': 1, 'c': 2, 'd': 1, 'e': 1, 'f': 1, 'g': 1}),
                Customer(name='Two', order={'c': 200, 'a': 1}),
                Customer(name='Three', order={'d': 3, 'g': 3}),
                Customer(name='Four', order={'e': 2}),
                Customer(name='Five', order={'a': 10}),
                Customer(name='Six', order={})
            ],
            [
                Store(name='1', inventory={'z': [10000.26, 1]}),
                Store(name='2', inventory={'b': [9.01, 5]}),
                Store(name='3', inventory={'a': [4.20, 7], 'f': [12.28, 3]}),
                Store(name='4', inventory={'b': [1.69, 1], 'e': [3.01, 10], 'c': [0.25, 4]})
            ])
