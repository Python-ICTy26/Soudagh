from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, Session
from scraputils import get_news


@route("/")
@route("/news")
def news_list():
    with Session.begin() as session:
        rows = session.query(News).filter(News.label == None).all()

        return template('news_template', rows=rows)


@route("/add_label")
def add_label():
    with Session.begin() as session:
        row = session.query(News).filter(News.id == request.query.id).first()
        row.label = request.query.label
        session.commit()
    redirect("/news")


@route("/update_news")
def update_news():
    news = get_news("https://news.ycombinator.com/newest")
    with Session.begin() as session:
        for new in news:
            if len(new.keys()) == 5 and not len(
                    session.query(News)
                    .filter(News.author == new["author"], News.title == new["title"])
                    .all()
            ):
                session.add(
                    News(
                        author=new["author"],
                        title=new["title"],
                        points=new["points"],
                        comments=new["comments"],
                        url=new["url"],
                    )
                )
        session.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    with Session.begin() as session:
        marked_news = session.query(News).filter(News.label is not None).all()
        marked_news = [[new.title, new.label] for new in marked_news]

        x_train = [n[0] for n in marked_news]
        y_train = [n[1] for n in marked_news]

        model = NaiveBayesClassifier(alpha=1)
        model.fit(x_train, y_train)

        news = session.query(News).filter(News.label is None).all()
        news_ids = [new.id for new in news]
        news = [new.title for new in news]
        predicts = model.predict(news)

        classified_news = {"good": [], "maybe": [], "never": []}

        for i, predict in enumerate(predicts):
            classified_news[predict].append(news_ids[i])

        rows = []
        for label in ["good", "maybe", "never"]:
            for id in classified_news[label]:
                rows.append(session.query(News).filter(News.id == id).first())
    return template("classification_template", rows=rows)


if __name__ == "__main__":
    run(host="localhost", port=8080)
