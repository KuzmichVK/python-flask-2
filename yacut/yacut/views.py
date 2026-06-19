from random import choices
from string import ascii_letters, digits

from flask import flash, redirect, render_template, url_for

from . import ID_LENGHT, app, db
from .forms import LinkForm
from .models import URLMap


def get_short_id():
    return "".join(choices(ascii_letters + digits, k=ID_LENGHT))


def get_unique_short_id():
    short_id = get_short_id()
    while URLMap.query.filter_by(short=short_id).first() is not None:
        short_id = get_short_id()
    return short_id


@app.route("/", methods=["GET", "POST"])
def index():
    form = LinkForm()
    if form.validate_on_submit():
        url = form.original_link.data
        short_id = form.custom_id.data
        if (
            short_id
            and URLMap.query.filter_by(short=short_id).first() is not None
        ):
            flash(f"Имя {short_id} уже занято!")
            return render_template("index.html", form=form)

        if not short_id:
            short_id = get_unique_short_id()
        new_link = URLMap(original=url, short=short_id)
        db.session.add(new_link)
        db.session.commit()
        short_url = url_for("index", _external=True) + short_id

        return render_template("index.html", form=form, short_url=short_url)
    return render_template("index.html", form=form)


@app.route("/<short_id>")
def redirect_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(link.original)
