import requests
import datetime


def get_date_number_of_days_ago(date):
    return datetime.date.today() - datetime.timedelta(days=date)


def get_trending_repositories(top_size, date):
    url = "https://api.github.com/search/repositories"
    formated_date = "{}{}".format("created:>=", date)
    parameters = {'q': formated_date, 'sort': 'stars', 'order': 'desc'}
    decoded_json = requests.get(url, params=parameters).json()
    top_repos = decoded_json["items"][:top_size]
    for repo in top_repos:
        yield repo


def get_repos_and_issues(top_repos):
    for rep in top_repos:
        issues_url = (rep["issues_url"].rstrip("{/number}"))
        parameters = {"state": "open"}
        issues = requests.get(
            issues_url, params=parameters).json()
        yield issues, rep


def print_top_repos(repos_and_issues):
    for issues, repo in repos_and_issues:
        print(
            "Ссылка: {}, звезды: {}, открытые вопросы: {}".format(
                repo["html_url"],
                repo["stargazers_count"],
                len(issues))
        )


if __name__ == "__main__":
    date = 7
    number_of_top_repos = 20
    last_date = get_date_number_of_days_ago(date)
    top_repos = get_trending_repositories(number_of_top_repos, last_date)
    repos_and_issues = get_repos_and_issues(top_repos)
    print_top_repos(repos_and_issues)
