from backend import create_app

app = create_app()


def __main():
    app.run(
        host="127.0.0.1",
        port=8080,
        debug=True,
        use_reloader=False,
    )


if __name__ == "__main__":
    __main()
