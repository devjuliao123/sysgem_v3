from app import create_app

app = create_app()

if __name__ == '__main__':
    print("SYSGEM Iniciando...")
    print("Acesse: http://127.0.0.1:5000/inicio")
    app.run(debug=True, host='0.0.0.0', port=5000)
