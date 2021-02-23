import os
import subprocess
import yaml
import argparse


def kaggle_settings():
    """kaggle_settings

    NOTE: This function is only usable in the kaggle notebook
    """
    from kaggle_secrets import UserSecretsClient

    user_secrets = UserSecretsClient()

    secret_dict = {}
    secret_dict['NEPTUNE_API_TOKEN'] = user_secrets.get_secret(
        'NEPTUNE_API_TOKEN')
    secret_dict['GITHUB_PAT'] = user_secrets.get_secret('GITHUB_PAT')

    for key, value in secret_dict.items():
        os.environ[key] = value


def colab_settings(dir_name='My Drive/keys', key_name='keys.yaml'):
    """colab_settings

    NOTE: This function is only usable in the google colab
    """

    from google.colab import auth
    from google.colab import drive

    # GCP
    auth.authenticate_user()

    # NEPTUNE, Github
    drive.mount('/content/drive')
    os.chdir(os.path.join('/content/drive', dir_name))

    with open(key_name) as f:
        secret_dict = yaml.safe_load(f)

    for key, value in secret_dict.items():
        os.environ[key] = value


def git_clone(github_https, user='tokuma09', token_env='GITHUB_PAT'):
    """git_clone

    Clone private repository using Personal Access Tokens

    Personal Access Tokens should be an environmental variable

    Parameters
    ----------
    github_https : str
        github https
    user : str, optional
        github user name, by default 'tokuma09'

    token_env : str, optional
        github personal access token, by default 'GITHUB_PAT'
    """
    # split repo
    owner = github_https.split('/')[-2]
    repo = github_https.split('/')[-1]

    from_path = 'https://{user}:{PAT}@github.com/{owner}/{repo_name}'

    repo_path = from_path.format(user=user,
                                 PAT=os.environ[token_env],
                                 owner=owner,
                                 repo_name=repo)

    subprocess.run(['git', 'clone', repo_path], shell=True)
    print('Successfully Cloned!')


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--github_url', '-g', help='Github URL')
    return parser.parse_args()


if __name__ == '__main__':

    args = get_arguments()

    if 'KAGGLE_URL_BASE' in set(os.environ.keys()):
        kaggle_settings()
        git_clone(args.github_url)

    elif 'COLAB_GPU' in set(os.environ.keys()):
        colab_settings()
        git_clone(args.github_url)
