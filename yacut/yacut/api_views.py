import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route("/api/id/", methods=["POST"])
def create_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    custom_id = data.get("custom_id")
    if custom_id:
        # Проверяем пользовательский идентификатор: длина и допустимые символы
        if not re.match(r"^[a-zA-Z0-9]{1,16}$", custom_id):
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки"
            )
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
    else:
        custom_id = get_unique_short_id()
    url_map = URLMap(original=data["url"], short=custom_id)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(
        {
            "url": url_map.original,
            "short_link": url_for(
                "redirect_url", short_id=url_map.short, _external=True
            ),
        }
    ), HTTPStatus.CREATED


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage("Указанный id не найден", HTTPStatus.NOT_FOUND)
    return jsonify({"url": url_map.original}), HTTPStatus.OK
