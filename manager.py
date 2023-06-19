from flask_app import create_app 

if __name__ == '__main__':
    app = create_app()
    # Run the Flask app on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)
