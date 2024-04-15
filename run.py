from app import run_app

if __name__=="__main__":
    app = run_app()
    server = app.server
    app.run_server(debug=False)