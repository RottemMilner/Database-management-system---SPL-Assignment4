import os
import sys
import Repository


def main(args):
    if len(args) < 5 or len(args) > 5:
        print("invalid input")
        return -1
    hats_list, suppliers_list = parse_input_conf(args[1])
    orders_list = parse_input_orders(args[2])
    repo = Repository.create(args[4])
    repo.create_tables()
    repo.insert_hats(hats_list)
    repo.insert_suppliers(suppliers_list)
    repo.execute_orders(orders_list)
    f = open(args[3], "a+")
    f.write(str(repo.output))


def parse_input_conf(config_path):
    with open(config_path) as input_f:
        rows = input_f.readlines()

    first_row = rows[0].split(",")
    num_of_hats = int(first_row[0])

    hats_list = []
    suppliers_list = []

    for row_num in range(1, len(rows)):
        curr_row = rows[row_num]
        curr_row = curr_row.replace('\n', '')
        curr_row_list = curr_row.split(",")
        if row_num <= num_of_hats:
            hats_list.append(curr_row_list)
        else:
            suppliers_list.append(curr_row_list)

    return hats_list, suppliers_list


def parse_input_orders(orders_path):
    with open(orders_path) as input_f:
        orders = input_f.readlines()

    orders_list = []
    for order in orders:
        order = order.replace('\n', '')
        orders_list.append(order.split(','))

    return orders_list


if __name__ == '__main__':
    main(sys.argv)

