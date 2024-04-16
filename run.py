from dash_app import create_app

app = create_app()
server = app.server
app.run_server(debug=False)