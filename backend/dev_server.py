import argparse
import os
import socketserver

from spa_handler import SpaFallbackHandler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_root)
    with socketserver.TCPServer(("", args.port), SpaFallbackHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
