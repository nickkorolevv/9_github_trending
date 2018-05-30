import requests
import datetime


def date_number_of_days_ago(days_number):
    return str(datetime.date.today() - datetime.timedelta(days=days_number))


def get_trending_repositories(top_size, days_number):
    url = "https://api.github.com/search/repositories"
    date = "{}{}".format("created:>=", days_number)
    parameters = {'q': date, 'sort': 'stars', 'order': 'desc'}
    response_from_github = requests.get(url, params=parameters).json()
    top_reps = response_from_github["items"][:top_size]
    return top_reps


def print_top_reps(top_reps):
    for rep in top_reps:
        print("URL: {}, звезды: {}, открытые задачи:{} ".format(
            rep["html_url"],
            rep["stargazers_count"],
            rep["open_issues_count"])
        )

if __name__ == "__main__":
    days_number = 7
    number_of_top_reps = 20
    days = date_number_of_days_ago(days_number)
    top_reps = get_trending_repositories(number_of_top_reps, days)
    print_top_reps(top_reps)
