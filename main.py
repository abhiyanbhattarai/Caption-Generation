from website import create_app

app = create_app()

app.config['PERMANENT_SESSION_LIFETIME'] = 600  # 10 minutes (adjust as needed)


if __name__ == '__main__':
    app.run(debug=True)

