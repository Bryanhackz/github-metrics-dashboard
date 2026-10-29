from wsgiref.simple_server import make_server
from router import application

def main() -> None:
    port = 8000
    with make_server("", port, application) as httpd:
        print(f"Serving on http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down.")

if __name__ == "__main__":
    main()