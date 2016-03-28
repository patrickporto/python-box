from websocket import Client

if __name__ == "__main__":
    try:
        ws = Client('ws://localhost:9000/', protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
