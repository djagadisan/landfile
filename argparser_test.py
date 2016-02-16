import argparse


def get_args():
    
    parser = argparse.ArgumentParser(prog='XXxx',
                        epilog='See "nova help COMMAND" '
                        'for help on a specific command.',
                        add_help=False)
    parser.add_argument('-h', '--help',
            action='store_true',
            help=argparse.SUPPRESS,
        )

    '''
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    subparsers = parser.add_subparsers()
    add_tenant = subparsers.add_parser('add', help='Add an allocation tenant')
    add_tenant.add_argument('-t', '-tenant_name', action='store',
                            required=True, help='Tenant Name'
                            )
    add_tenant.set_defaults(func='add')
    key_update = subparsers.add_parser('keystone-update',
                                       help='Update tenant details'
                                       )
    key_update.add_argument('-t', '-tenant', action='store',
                            required=True, help='Tenant Name/ID'
                            )
    key_update.set_defaults(func='keystone_update')
    '''
    return parser


    def get_subcommand_parser():
        parser = get_args()

        subparsers = parser.add_subparsers(metavar='<subcommand>')
        
        set_command(subparsers)
        return parser
    
    def set_command():
        
        