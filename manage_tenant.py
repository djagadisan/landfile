#!/usr/bin/env python
from manage_tenant_util import select_options
from manage_tenant_options import get_args


def main():

    args_data = get_args()
    select_options(args_data, args_data.func)

if __name__ == '__main__':
    main()
