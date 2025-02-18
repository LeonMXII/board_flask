
from flask import Flask, jsonify, request, Response
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from errors import HttpError
from models import Session, Board
from schema import validate_json, CreateBoard

app = Flask("app")
app.config['JSON_AS_ASCII'] = False

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response: Response):
    request.session.close()
    return response

@app.errorhandler(HttpError)
def error_heandler(err: HttpError):
    http_response = jsonify({"error": err.message})
    http_response.status_code = err.status_code
    return http_response

def get_board_id(board_id: int):
    board = request.session.get(Board, board_id)
    if board is None:
        raise HttpError(404, "Объявление не найдено!")
    return board

def add_board(board: Board):
    try:
        request.session.add(board)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, message="Объявление уже существует!")
class BoardView(MethodView):
    def get(self, board_id: int):
        board = get_board_id(board_id)
        return jsonify(board.dict)

    def post(self):
        json_data = validate_json(CreateBoard, request.json)
        board = Board(
            title=json_data["title"],
            description=json_data["description"],
            owner=json_data["owner"]
        )
        add_board(board)
        return jsonify(board.id_dict)

    def delete(self, board_id: int):
        board = get_board_id(board_id)
        request.session.delete(board)
        request.session.commit()
        return jsonify({"status": "Объявление удалено!"})


board_view = BoardView.as_view("board_view")
app.add_url_rule("/api/v1/board", view_func=board_view, methods=["POST"])
app.add_url_rule("/api/v1/board/<int:board_id>", view_func=board_view, methods=["GET", "DELETE"])

if __name__ == "__main__":
    app.run(port=5050, debug=True)