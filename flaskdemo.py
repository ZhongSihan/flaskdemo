from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")


@app.route('/results')
def results():
    search_term = session.get('search_term', '')
    page = get_page(search_term)
    return render_template("results.html", term=search_term, page=page)


def get_page(search_term):
    try:
        return wikipedia.page(search_term)
    except wikipedia.exceptions.PageError:
        return wikipedia.page(wikipedia.random())
    except wikipedia.exceptions.DisambiguationError:
        page_titles = wikipedia.search(search_term)
        title = page_titles[2] if page_titles[1].lower() == page_titles[0].lower() else page_titles[1]
        return get_page(title)


if __name__ == '__main__':
    app.run(debug=True)
