import argparse


def get_args():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    subparsers = parser.add_subparsers()
    add_tenant = subparsers.add_parser('add', help='Add an allocation tenant')
    add_tenant.add_argument('-t', '-tenant_name', action='store',
                            required=True, help='Tenant Name'
                            )
    add_tenant.add_argument('-d', '-tenant_desc', action='store', nargs=1,
                            default=None, help='Tenant description'
                            )
    add_tenant.add_argument('-e', '-user_email', action='store',
                            required=True, help='User email'
                            )
    add_tenant.add_argument('-c', '-cores', action='store', type=int,
                            required=True, help='Number or cores'
                            )
    add_tenant.add_argument('-i', '-instances', action='store',
                            required=True, type=int,
                            help='Number of instances'
                            )
    add_tenant.add_argument('-a', '-allocation_id', action='store',
                            required=True, type=str,
                            help='Allocation id'
                            )

    add_tenant.add_argument('-v', '-volumes', action='store',
                            required=False, type=int,
                            help='Volumes (GB)(includes the snapshot)'
                            )
    add_tenant.add_argument('-g', '-gigabytes', action='store',
                            required=False, type=int,
                            help='Gigabyes (GB)'
                            )
    add_tenant.set_defaults(func='add')

    key_update = subparsers.add_parser('keystone-update',
                                       help='Update tenant details'
                                       )
    key_update.add_argument('-t', '-tenant', action='store',
                            required=True, help='Tenant Name/ID'
                            )
    key_update.add_argument('-d', '-description', action='store',
                            type=str, required=False,
                            help='Tenant description'
                            )
    key_update.add_argument('-a', '-allocation_id', action='store',
                            type=str, required=False,
                            help='Allocation ID'
                            )
    key_update.add_argument('-v', '-vicnode_id', action='store',
                            type=str, required=False,
                            help='VicNode ID'
                            )
    key_update.add_argument('-n', '-name', action='store',
                            type=str, required=False,
                            help='Tenant Name'
                            )
    key_update.add_argument('-e', '-enable', action='store', type=bool,
                            required=False, help='Enable <True|False>'
                            )
    key_update.set_defaults(func='keystone_update')

    nova_update = subparsers.add_parser('nova-update',
                                        help='Update nova quotas for tenant'
                                        )
    nova_update.add_argument('-t', '-tenant', action='store',
                             required=True, help='Tenant Name/ID'
                             )
    nova_update.add_argument('-c', '-cores', action='store', type=int,
                             required=False, help='Number or cores'
                             )
    nova_update.add_argument('-i', '-instances', action='store',
                             required=False, type=int,
                             help='Number of instances'
                             )
    nova_update.set_defaults(func='nova_update')

    cinder_update = subparsers.add_parser('cinder-update',
                                          help='Volumes update for tenant'
                                          )
    cinder_update.add_argument('-t', '-tenant', action='store',
                               required=True, help='Tenant Name/ID'
                               )
    cinder_update.add_argument('-g', '-gigabytes', action='store', type=int,
                               required=False, help='Total volumes (GB)'
                               )
    cinder_update.add_argument('-v', '-volumes', action='store',
                               required=False, type=int,
                               help='Max size for a volumes (GB)'
                               )
    cinder_update.add_argument('-s', '-snapshot', action='store',
                               required=False, type=int,
                               help='Max size for a snapshot (GB)'
                               )
    cinder_update.set_defaults(func='cinder_update')

    info_tenant = subparsers.add_parser('info',
                                        help='tenant details'
                                        )
    info_tenant.add_argument('-t', '-tenant', action='store',
                             required=True, help='Tenant Name/ID'
                             )
    info_tenant.set_defaults(func='search')

    batch_process = subparsers.add_parser('email', help='process from email')
    batch_process.add_argument('-s', '-string', action='store',
                               required='True', help='e.g.[t1,x@x.co,8,4,100]')
    batch_process.set_defaults(func='email')


    args = vars(parser.parse_args())
    if args['func'] is 'nova_update' or args['func'] is 'keystone_update':
        check_options = [v for v in args.values() if v is None]
        if len(check_options) == 2:
            parser.error("Update requires at least one optional argument")
    elif args['func'] is 'cinder_update':
# elif args['func'] is 'keystone_update' or args['func'] is 'cinder_update':
        check_options = [v for v in args.values() if v is None]
        if len(check_options) == 3:
            parser.error("Update requires at least one optional argument")

    return parser.parse_args()
