import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    serve_parser = subparsers.add_parser('serve', help='run application in debug mode with hot reload')
    serve_parser.add_argument('--host', type=str, default='0.0.0.0')
    serve_parser.add_argument('--port', type=int, default=5000)

    start_parser = subparsers.add_parser('start', help='run application in production mode (gunicorn)')
    start_parser.add_argument('--host', type=str, default='0.0.0.0')
    start_parser.add_argument('--port', type=int, default=5000)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        exit(0)
    return args


def main():
    args = parse_args()

    if args.command == 'serve':
        from .server import wsgi_app
        wsgi_app.run(host=args.host, port=args.port)
    elif args.command == 'start':
        import subprocess
        subprocess.call(['gunicorn', '-b', f'{args.host}:{args.port}', 'apartment_backend.server:wsgi_app'])


if __name__ == '__main__':
    main()
