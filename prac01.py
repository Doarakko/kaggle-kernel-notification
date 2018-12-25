from kaggle.api.kaggle_api_extended import KaggleApi


def get_kernels_list(competition_name=None):
    api = KaggleApi()
    api.authenticate()
    return api.kernels_list(competition=competition_name, sort_by='dateCreated')


def post_slack(message='')



def main():
    competition_name = 'elo-merchant-category-recommendation'
    kernels_list = get_kernels_list(competition_name)
    post_slack(kernels_list=kernels_list)

main()
